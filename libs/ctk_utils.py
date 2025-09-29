# -*- coding: UTF-8 -*-

import sys
import os

import tkinter as tk
import customtkinter as ctk

#pip install CTkMessagebox
import CTkMessagebox
from CTkMessagebox import CTkMessagebox
from customtkinter import filedialog


from str import *
from bytes import *
from files import *
from pathlib import Path 
from log import *

#tkinter.NORMAL/customtkinter.NORMAL/"normal" -> habilita el entry
ctk_utils_Def_enabled = "normal"
#tkinter.DISABLED/customtkinter.DISABLED/"disabled" -> deshabilita el entry
ctk_utils_Def_disabled = "disabled"

#COLORS
ctk_utils_color_background_light = "#EEEEEE"
ctk_utils_color_background_dark = "#222222"
ctk_utils_color_dark_button = "#444444"
ctk_utils_color_red_dark = "#FF5555"
ctk_utils_color_green_dark = "#44FF44"
ctk_utils_color_blue_dark = "#0818A8"

#FONT
ctk_utils_Font = "Courier New"
ctk_utils_FontSize = 14

# NOT WORKING AS EXPECTED: 2025-05-15
# AFTER SELECTING YES/NO IT IS NOT POSSIBLE TO GET THE GLOBAL VARIABLE RESULT IN ANOTHER .PY
#DISPLAY WINDOW
ctk_utils_show_windowYESNOResult = ""
ctk_utils_window = None

#---------------------------------------------------------------------------------------------------------
# ctk_utils_TextBoxSet => Setting value from init in a CTkTextbox
#---------------------------------------------------------------------------------------------------------
def ctk_utils_TextBoxSet(obj, Value):
    ctk_utils_ObjEnable(obj)
    obj.delete(0.0, 'end')
    obj.insert(ctk.INSERT,  Value)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_TextBoxAppend => Adding value at the end of a CTkTextbox
#---------------------------------------------------------------------------------------------------------
def ctk_utils_TextBoxAppend(obj, Value):
    ctk_utils_ObjEnable(obj)
    obj.insert(ctk.END,  Value)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_CTkTextboxGetData => Get data from an object, for example CTkTextbox 
#---------------------------------------------------------------------------------------------------------
def ctk_utils_CTkTextboxGetData(obj):
    sReturn = obj.get("1.0",'end-1c')
    return sReturn

#---------------------------------------------------------------------------------------------------------
# ctk_utils_CTkLabelGetText => Get text from a label 
#---------------------------------------------------------------------------------------------------------
def ctk_utils_CTkLabelGetText(obj):
    sReturn = obj.cget("text")
    return sReturn

#---------------------------------------------------------------------------------------------------------
# ctk_utils_CTkLabelSetText => Set text to a label 
#---------------------------------------------------------------------------------------------------------
def ctk_utils_CTkLabelSetText(obj, sData):
    obj.configure(text = sData)
    return sData

#---------------------------------------------------------------------------------------------------------
# ctk_utils_CTkComboBoxGetData => Get data from an object, for example CTkComboBox
#---------------------------------------------------------------------------------------------------------
def ctk_utils_CTkComboBoxGetData(obj):
    return ctk_utils_ObjGetData(obj)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_CTkComboBoxSetData => Set data for an object, for example CTkComboBox
#---------------------------------------------------------------------------------------------------------
def ctk_utils_CTkComboBoxSetData(obj, data):
    return ctk_utils_ObjSetData(obj, data)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjGetData => Get data from an object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjGetData(obj):
    sReturn = obj.get()
    return sReturn

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjSetData => Set data from an object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjSetData(obj, data):
    obj.set(data)
    return data

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ButtonSetText => Setting value to a CTkButton
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ButtonSetText(obj, sCaption):
    obj.configure(text=sCaption)
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjEnable => Setting Enable Object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjEnable(obj):
    ctk_utils_ObjEnableDisable(obj, True)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjDisable => Setting Disable Object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjDisable(obj):
    ctk_utils_ObjEnableDisable(obj, False)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjEnableDisable => Setting Enable/Disable Object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjEnableDisable(obj, bEnable=True):
    if bEnable:
       obj.configure(state=ctk_utils_Def_enabled)
    else:
       obj.configure(state=ctk_utils_Def_disabled)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_WindowsEnable => Enable Window
#---------------------------------------------------------------------------------------------------------
def ctk_utils_WindowsEnable(windw):
    ctk_utils_WindowsEnableDisable(windw, True)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_WindowsDisable => Disable Window
#---------------------------------------------------------------------------------------------------------
def ctk_utils_WindowsDisable(windw):
    ctk_utils_WindowsEnableDisable(windw, False)
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_WindowsEnableDisable => Enable/Disable Window
#---------------------------------------------------------------------------------------------------------
def ctk_utils_WindowsEnableDisable(wdw, bEnable=True):
    if file_IsOSLinux():
       if bEnable:
           wdw.grab_set()
       else:
           wdw.grab_release()
    else:
       if bEnable:
          wdw.attributes('-disabled', False)
       else:
          wdw.attributes('-disabled', True)
       
#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjSetColor => Setting Color for object.
# It can be a string such as "green" or the value itself color_green_dark = "#44FF44"
# Example: ctk_utils_ObjSetColor(self.response_tpda.configure, "green")
# Example: ctk_utils_ObjSetColor(self.response_tpda.configure, "#44FF44")
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjSetColor(obj, Color):
    obj.configure(text_color=Color)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_show_window_Info => Showing Dialog Box with Information
#---------------------------------------------------------------------------------------------------------
def ctk_utils_show_window_Info(message):
    ctk_utils_show_window(message, "Message")
      
#---------------------------------------------------------------------------------------------------------
# ctk_utils_show_window_Error => Showing Dialog Box with Error
#---------------------------------------------------------------------------------------------------------
def ctk_utils_show_window_Error(message, bFocus=True):
    ctk_utils_show_window(message, "error", bFocus)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_show_window_OK => Showing Dialog Box with OK
#---------------------------------------------------------------------------------------------------------
def ctk_utils_show_window_OK(message, bFocus=True):
    ctk_utils_show_window(message, "ok", bFocus)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_show_windowYESNO => Result of Showing Dialog Box => YES=True/NO=False
#---------------------------------------------------------------------------------------------------------
def ctk_utils_show_windowYESNO(sResult):
    # GLOBAL VARIABLE TO SAVE RESULT
    global ctk_utils_show_windowYESNOResult
    ctk_utils_show_windowYESNOResult = sResult
    
    print("ctk_utils_show_windowYESNO - ctk_utils_show_windowYESNOResult = " + str(ctk_utils_show_windowYESNOResult))
    
    if not ctk_utils_window is None:
       ctk_utils_window.destroy()

    print("ctk_utils_show_windowYESNO - ctk_utils_show_windowYESNOResult = " + str(ctk_utils_show_windowYESNOResult))
       
    return ctk_utils_show_windowYESNOResult
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_setTextBox => Showing Dialog Box
#---------------------------------------------------------------------------------------------------------
#def ctk_utils_show_window(message, sTitle = "", bButtonYesNo=False):
def ctk_utils_show_window(message, sTitle = "", bFocus=True):
    
    if message == "":
       return 
    
    # GLOBAL VARIABLE TO SAVE RESULT
    global ctk_utils_show_windowYESNOResult
    ctk_utils_show_windowYESNOResult = ""

    window = ctk.CTkToplevel()       

    msg_background_color = (ctk_utils_color_background_light, ctk_utils_color_background_dark)
    msg_button_color = ("orange", ctk_utils_color_dark_button)  
    msg_button_color_text = ("black", "white")
    
    msg_Font = ctk_utils_Font
    msg_FontSize = ctk_utils_FontSize
    
    msg_color_OK = ("green", ctk_utils_color_green_dark)
    msg_color_NOK = ("red", ctk_utils_color_red_dark)
    msg_color_INFO = ("blue", ctk_utils_color_green_dark)
   
    msg_color = msg_color_INFO

    if (sTitle.lower() == "error"):
       window.title("Error")
       msg_color = msg_color_NOK
    else:
       if (sTitle.lower() == "ok"):
          window.title("Processed Successfully")
          msg_color = msg_color_OK
       else:
          if (sTitle.lower() == ""):
             window.title("Message")
          else:
             window.title(sTitle)

    nWidth = window.winfo_width() * 3
    windows_height = window.winfo_height()

    #print("show_window - window.winfo_width(): " + str(window.winfo_width()))
    #print("show_window - len(message): " + str(len(message)))
    if len(message) > 100:
       nWidth = nWidth * 2
       windows_height = windows_height * 1.5
       
    #print("show_window - nWidth: " + str(nWidth))
    window_width = nWidth

    window.geometry(f"{window_width}x{windows_height}")
               
    #window.Label(window, text = message, font=("Georgia", 14)).pack(pady=20)
    label = ctk.CTkLabel(window, text = message, fg_color = msg_background_color, font=(msg_Font, msg_FontSize), text_color=msg_color)
    label.pack(padx=20)
    #window.Button(window, text="Close this window", command=window.destroy).pack(pady=10)
    
    # NOT WORKING AS EXPECTED: 2025-05-15
    # AFTER SELECTING YES/NO IT IS NOT POSSIBLE TO GET THE GLOBAL VARIABLE RESULT IN ANOTHER .PY
    #if bButtonYesNo:
    #   yesno_frame = ctk.CTkFrame(window, border_width=2)  # Contenedor para agrupar los widgets
    #   yesno_frame.pack(anchor="w", pady=5)  # Alinear el frame a la izquierda
    #   #lambda meaning:
    #   #So in the case of buttons, lambda basically delays the execution of the function until the user clicks the button, 
    #   #by creating another function on the spot, which does not get called until the button is actually clicked. 
    #   buttonYES = ctk.CTkButton(yesno_frame, text="Yes", command=lambda: ctk_utils_show_windowYESNO("YES"), fg_color=msg_button_color, text_color=msg_button_color_text)
    #   buttonYES.pack(side="left", padx=30, pady=10)
    #   buttonNO = ctk.CTkButton(yesno_frame, text="No", command=lambda: ctk_utils_show_windowYESNO("NO"), fg_color=msg_button_color, text_color=msg_button_color_text)
    #   buttonNO.pack(side="left", padx=10, pady=10)
    #else:
    #   button = ctk.CTkButton(window, text="Close this window", command=window.destroy, fg_color=msg_button_color, text_color=msg_button_color_text)
    #   button.pack(pady=10)

    button = ctk.CTkButton(window, text="Close this window", command=window.destroy, fg_color=msg_button_color, text_color=msg_button_color_text)
    button.pack(pady=10)
    
    window.update_idletasks()
        
    window.update()
    
    if bFocus:
       window.focus()

    window.after(100, window.lift) # Workaround for bug where main window takes focus

    # GLOBAL VARIABLE FOR WINDOWS
    #global ctk_utils_window
    #ctk_utils_window = window
    
    #if bButtonYesNo:
    #   ctk_utils_window.mainloop()
       
    return    

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBoxError => Showing Message Box with Error
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBoxError(sTitle, sMessage):
    ctk_utils_MsgBox(sTitle, sMessage, "error")

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBoxError => Showing Message Box with Warning
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBoxWarning(sTitle, sMessage):
    ctk_utils_MsgBox(sTitle, sMessage, "warning")

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBoxError => Showing Message Box with Info
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBoxInfo(sTitle, sMessage):
    ctk_utils_MsgBox(sTitle, sMessage)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBoxError => Showing Message Box with Warning
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBoxWarning(sTitle, sMessage):
    ctk_utils_MsgBox(sTitle, sMessage, "warning")

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBox => Showing Message Box
# https://pypi.org/project/CTkMessagebox/
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBox(sTitle, sMessage, sIcon="check"):
    # Default messagebox for showing some information
    CTkMessagebox(title=sTitle, message=sMessage, icon=sIcon)
    

#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBoxQuestion => Showing Message Box with a Question
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBoxQuestion(sTitle, sMessage, bYesFirst=True):

    try:
       if bYesFirst:
          msg = CTkMessagebox(title=sTitle, message=sMessage, icon="question", option_1="Cancel", option_2="No", option_3="Yes")
       else:
          msg = CTkMessagebox(title=sTitle, message=sMessage, icon="question", option_1="Cancel", option_2="Yes", option_3="No")

       return msg.get()

    except Exception as e:
        sError = "ctk_utils_MsgBoxQuestion. An unexpected error has occurred. " + str(e) 
        log_writePrintOnlyError(sError)
        return str(e)
       
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_MsgBox => Showing Message Box
#---------------------------------------------------------------------------------------------------------
def ctk_utils_MsgBox(sTitle, sMessage, sIcon="check"):
    #CTkMessagebox(title=sTitle, message=sMessage, icon=sIcon, option_1="Close")
    CTkMessagebox(title=sTitle, message=sMessage, option_1="Close")
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_GetWindowWidth => Getting window width 
#---------------------------------------------------------------------------------------------------------
def ctk_utils_GetWindowWidth(tkWindowMaster):
    nWidth, nHeight = ctk_utils_GetWindowWidthHeight(tkWindowMaster)
    return nWidth

#---------------------------------------------------------------------------------------------------------
# ctk_utils_GetWindowHeight => Getting window height 
#---------------------------------------------------------------------------------------------------------
def ctk_utils_GetWindowHeight():
    nWidth, nHeight = ctk_utils_GetWindowWidthHeight(tkWindowMaster)
    return nHeight
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_setTextBox => Getting window width and height
# Example: self.nWindowWidth, self.nWindowHeight = ctk_utils_GetWindowWidthHeight(self.main_window)
#---------------------------------------------------------------------------------------------------------
def ctk_utils_GetWindowWidthHeight(tkWindowMaster):
    nWidth = tkWindowMaster.winfo_screenwidth()
    nHeight = tkWindowMaster.winfo_screenheight()
    return nWidth, nHeight
             
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# ctk_utils_ObjSetFocus => Setting focus to an object
#---------------------------------------------------------------------------------------------------------
def ctk_utils_ObjSetFocus(obj):
    obj.focus_set()        
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_WindowsClose => Close a Window
#---------------------------------------------------------------------------------------------------------
def ctk_utils_WindowsClose(tkWindows):
    tkWindows.withdraw()
    tkWindows.quit()


#---------------------------------------------------------------------------------------------------------
# ctk_utils_AskOpenFileName_Files_IJC_CAP =>Open Custom TKinter Dialog for selecting one or more files with IJC and CAP files
#---------------------------------------------------------------------------------------------------------
def ctk_utils_AskOpenFileName_Files_IJC_CAP(sPath, sTitle="", bMultipleFiles=False):
    sType = "applets"
    if bMultipleFiles:
        return ctk_utils_AskOpenMultipleFileNames(sPath, sTitle, sType, True)
    else:
        return ctk_utils_AskOpenFileName(sPath, sTitle, sType)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_AskOpenFileName_Files_CSV =>Open Custom TKinter Dialog for selecting one or more files with CSV files
#---------------------------------------------------------------------------------------------------------
def ctk_utils_AskOpenFileName_Files_CSV(sPath, sTitle="", bMultipleFiles=False):
    sType = "csv"
    if bMultipleFiles:
        return ctk_utils_AskOpenMultipleFileNames(sPath, sTitle, sType, True)
    else:
        return ctk_utils_AskOpenFileName(sPath, sTitle, sType)

#---------------------------------------------------------------------------------------------------------
# ctk_utils_AskOpenFileName_Files_XML =>Open Custom TKinter Dialog for selecting one or more files with XML files
#---------------------------------------------------------------------------------------------------------
def ctk_utils_AskOpenFileName_Files_XML(sPath, sTitle="", bMultipleFiles=False):
    sType = "xml"
    if bMultipleFiles:
        return ctk_utils_AskOpenMultipleFileNames(sPath, sTitle, sType, True)
    else:
        return ctk_utils_AskOpenFileName(sPath, sTitle, sType)
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_AskOpenFileName => Open Custom TKinter Dialog for selecting a file
# Example for file_types:
# file_types = [("IJC Files", "*.ijc"), ("CAP Files", "*.cap"), ("Text Files", "*.txt"), ("All Files", "*.*")]
# file_types = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
#---------------------------------------------------------------------------------------------------------
def ctk_utils_AskOpenFileName(sPath, sTitle="", file_types=""):
    sReturn = ""
    lstFiles = ctk_utils_AskOpenMultipleFileNames(sPath, sTitle, file_types)
    if len(lstFiles) > 0:
       sReturn = lstFiles[0]
    
    return sReturn
       
#---------------------------------------------------------------------------------------------------------
# ctk_utils_AskOpenMultipleFileNames => Open Custom TKinter Dialog for selecting one or more files
# Example for file_types:
# file_types = [("IJC Files", "*.ijc"), ("CAP Files", "*.cap"), ("Text Files", "*.txt"), ("All Files", "*.*")]
# file_types = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
#---------------------------------------------------------------------------------------------------------
def ctk_utils_AskOpenMultipleFileNames(sPath, sTitle="", file_types="", bMultipleFiles=False):
    
    if sPath == "":
       sPath = os.path.dirname(os.path.realpath(__file__)) 

    if file_types=="":    
       file_types = [("Text Files", "*.txt"), ("All Files", "*.*")]
       
    if str(file_types).lower() == "applets":
       file_types = [("IJC Files", "*.ijc"), ("CAP Files", "*.cap"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    if str(file_types).lower() == "csv":
       file_types = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    if str(file_types).lower() == "xml":
       file_types = [("XML Files", "*.xml"), ("Text Files", "*.txt"), ("All Files", "*.*")]
       
    if sTitle == "":
       sTitle = "Select File"

    #print("file_types = " + str(file_types))
    
    returnFilesLst = []
    if bMultipleFiles:
         returnFilesLst = filedialog.askopenfilenames(
                   initialdir=sPath, 
                   title=sTitle,
                   filetypes=file_types
                   )
    
    else:      
         filename = filedialog.askopenfilename(
                   initialdir=sPath, 
                   title=sTitle,
                   filetypes=file_types
                   )
         returnFilesLst.append(filename)          
    
    #print("ctk_utils_AskOpenMultipleFileNames - returnFilesLst = " + str(returnFilesLst))
    
    #FOR TESTING
    #bMultipleFiles = False
    #lst = ctk_utils_AskOpenFileName_Files_IJC_CAP(current, "One IJC", bMultipleFiles)
    #print("One File - ijc: " + str(lst))
    #bMultipleFiles = True
    #lst = ctk_utils_AskOpenFileName_Files_IJC_CAP(current, "One IJC", bMultipleFiles)
    #print("Multiple Files - ijc: " + str(lst) + " - Len: " + str(len(lst)))
    #exit(0)

    return returnFilesLst

#---------------------------------------------------------------------------------------------------------
# ctk_utils_FocusOnWindow =>Set focus on a window
#---------------------------------------------------------------------------------------------------------
def ctk_utils_FocusOnWindow(window):
    window.focus_force()
    
    
#---------------------------------------------------------------------------------------------------------
# ctk_utils_TextBoxSet => Setting value from init in a CTkTextbox
#---------------------------------------------------------------------------------------------------------
def ctk_utils_WindowsSetBitmap(window, app_ico, bAddImagesDir=True):

    try:

        sImagesDir = ""
        if bAddImagesDir:
           sImagesDir = "Images"
      
        icon_path = ""   
        if file_fFileIsExe():
           if sImagesDir != "":
              icon_path = os.path.join(sys._MEIPASS, sImagesDir + '/', app_ico)
           else:
              icon_path = os.path.join(sys._MEIPASS, app_ico)
              
        else:  # Si esta corriendo como script
           project_root = Path(__file__).resolve().parents[2]  # Subir dos niveles desde la ubicacion actual
           if sImagesDir != "":
              icon_path = project_root / sImagesDir / app_ico
           else:   
              icon_path = project_root / app_ico
        
        icon_path = file_fNormalPathForWindowsLinux(icon_path)  
        if not file_IsOSLinux():
           window.iconbitmap(icon_path)  # Usar ruta absoluta

        return True
        
    except Exception as e:
        sError = "An unexpected error has occurred. " + str(e) 
        log_writePrintOnlyError(sError)
        return False

#---------------------------------------------------------------------------------------------------------
# ctk_utils_open_files => Open a 
#---------------------------------------------------------------------------------------------------------

# # # ?? Example 1: Select multiple XML or TXT files for input processing
# # files = ctk_utils_open_files(
# #     filetypes=[("XML and TXT files", "*.xml *.txt")],
# #     title="Select input files",
# #     initialdir="C:/Documents/data",
# #     multiple=True
# # )

# # # ?? Example 2: Select a single CSV file to load configuration or keys
# # file = ctk_utils_open_files(
# #     filetypes=[("CSV files", "*.csv")],
# #     title="Select transport key file",
# #     initialdir="C:/keys",
# #     multiple=False
# # )

# # # ??? Example 3: Allow user to select multiple images (PNG, JPG) for batch processing
# # images = ctk_utils_open_files(
# #     filetypes=[("Image files", "*.png *.jpg *.jpeg")],
# #     title="Select images to process",
# #     initialdir="~/Pictures",
# #     multiple=True
# )
def ctk_utils_open_files(filetypes, title="Select File(s)", initialdir=".", multiple=True):
    if multiple:
        return filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetypes)
    else:
        return filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)
    
#---------------------------------------------------------------------------------------------------------
#-------CTkTextSearch-------------------------------------------------------------------------------------
# USAGE:
# self.history_search = CTkTextSearch(self, self.history_box) -> Add search dialog with Ctrl+F
# self.history_search = CTkTextSearch(self, self.history_box, clear_highlight_on_close=False) -> Keep highlights after closing dialog
# self.history_search = CTkTextSearch(self, self.history_box, inline_frame=self.search_frame) -> Inline search bar in existing frame
#---------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
class CTkTextSearch:
    """
    Search and highlight text in a CTkTextbox.
    Can work in:
      - Dialog mode (Ctrl+F popup window)
      - Inline mode (embedded in an existing frame)
    """

    def __init__(self, parent, textbox: ctk.CTkTextbox, clear_highlight_on_close=True, inline_frame=None):
        self.parent = parent
        self.textbox = textbox
        self.clear_highlight_on_close = clear_highlight_on_close
        self._tag_name = "search_highlight"

        # setup highlight tag
        try:
            self.textbox.tag_config(self._tag_name, background="yellow", foreground="black")
        except Exception:
            pass

        if inline_frame:
            self._add_inline_search(inline_frame)
        else:
            self._add_bindings()

    def _add_bindings(self):
        # Ctrl+F triggers dialog
        self.parent.bind("<Control-f>", self._open_search_dialog)

    def _add_inline_search(self, frame):
        """Attach inline search bar inside given frame"""
        self.entry = ctk.CTkEntry(frame, placeholder_text="Search...")
        self.entry.pack(side="left", padx=5)

        def do_find(event=None):
            self._clear_highlight()
            word = self.entry.get()
            if not word:
                return
            idx = "1.0"
            first_match = None
            while True:
                idx = self.textbox.search(word, idx, nocase=1, stopindex="end")
                if not idx:
                    break
                lastidx = f"{idx}+{len(word)}c"
                self.textbox.tag_add(self._tag_name, idx, lastidx)
                if first_match is None:
                    first_match = idx
                idx = lastidx
            if first_match:
                self.textbox.see(first_match)
            else:
                ctk_utils_MsgBoxInfo("Not found", f'"{word}" not found in text.')

        self.search_button = ctk.CTkButton(frame, text="Find", width=60, command=do_find)
        self.search_button.pack(side="left", padx=5)
        self.entry.bind("<Return>", do_find)

    def _open_search_dialog(self, event=None):
        top = ctk.CTkToplevel(self.parent)
        top.title("Find text")
        top.geometry("300x100")
        top.grab_set()

        def on_close():
            if self.clear_highlight_on_close:
                self._clear_highlight()
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", on_close)

        entry = ctk.CTkEntry(top)
        entry.pack(fill="x", padx=10, pady=10)
        entry.focus_set()

        def do_find(event=None):
            self._clear_highlight()
            word = entry.get()
            if not word:
                return
            idx = "1.0"
            first_match = None
            while True:
                idx = self.textbox.search(word, idx, nocase=1, stopindex="end")
                if not idx:
                    break
                lastidx = f"{idx}+{len(word)}c"
                self.textbox.tag_add(self._tag_name, idx, lastidx)
                if first_match is None:
                    first_match = idx
                idx = lastidx
            if first_match:
                self.textbox.see(first_match)
            else:
                ctk_utils_MsgBoxInfo("Not found", f'"{word}" not found in text.')

        ctk.CTkButton(top, text="Find", command=do_find).pack(pady=5)
        entry.bind("<Return>", do_find)

    def _clear_highlight(self):
        self.textbox.tag_remove(self._tag_name, "1.0", "end")
#---------------------------------------------------------------------------------------------------------
#-------CTkTextWithLineNumbers--------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 1) Create and pack:
#
#   import customtkinter as ctk
#   root = ctk.CTk()
#   console = CTkTextWithLineNumbers(root, font=("Consolas", 12), height=320)
#   console.pack(fill="both", expand=True, padx=10, pady=10)
#
# 2) Append one line (auto-scroll both panes):
#
#   def append_line(s: str):
#       if not s.endswith("\n"):
#           s += "\n"
#       console.text.configure(state="normal")
#       console.text.insert("end", s)
#       console.text.configure(state="disabled")
#       console.see_end()              # keeps line numbers in sync with content
#
#   append_line("hello world")
#
# 3) Bulk add lines efficiently:
#
#   console.text.configure(state="normal")
#   console.text.insert("end", "\n".join(f"line {i}" for i in range(1, 101)) + "\n")
#   console.text.configure(state="disabled")
#   console.see_end()
#
# 4) Clear all content and refresh numbers:
#
#   console.text.configure(state="normal")
#   console.text.delete("1.0", "end")
#   console.text.configure(state="disabled")
#   console._update_line_numbers()    # required after external edits
#
# 5) Replace entire content:
#
#   console.text.configure(state="normal")
#   console.text.delete("1.0", "end")
#   console.text.insert("1.0", "Header\n------\nA\nB\nC\n")
#   console.text.configure(state="disabled")
#   console.see_end()
#
# 6) Read current text:
#
#   data = console.text.get("1.0", "end-1c")
#
# 7) Programmatic scroll to bottom later:
#
#   console.see_end()
#
# 8) Optional: disable user edits (read-only view):
#
#   console.text.configure(state="disabled")    # re-enable with "normal" before inserts
#
# 9) Pack into an existing frame instead of root:
#
#   console = CTkTextWithLineNumbers(parent_frame, font=("Consolas", 12))
#   console.pack(fill="both", expand=True)
#
# root.mainloop()
# -----------------------------------------------------------------------------
class CTkTextWithLineNumbers(ctk.CTkFrame):
    def __init__(self, master, font=("Consolas", 12), **kwargs):
        super().__init__(master)
        self.font = font

        # gutter
        self.line_numbers = ctk.CTkTextbox(
            self,
            width=60,
            state="disabled",
            font=self.font,
            wrap="none",
            fg_color=("#f0f0f0", "#2b2b2b"),
            text_color=("black", "white"),
            activate_scrollbars=False
        )
        self.line_numbers.pack(side="left", fill="y")

        # main text
        self.text = ctk.CTkTextbox(self, font=self.font, wrap="none", **kwargs, activate_scrollbars=False)
        self.text.pack(side="right", fill="both", expand=True)

        # scroll sync
        self.text.configure(yscrollcommand=self._on_scroll)
        self.line_numbers.configure(yscrollcommand=self._on_scroll)

        # events
        self.text.bind("<<Modified>>", self._on_change)
        self.text.bind("<KeyRelease>", self._on_change)

    def _on_scroll(self, *args):
        # keep both views aligned
        self.line_numbers.yview_moveto(self.text.yview()[0])
        return

    def _on_change(self, event=None):
        self.text.edit_modified(0)
        self._update_line_numbers()

    def _update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")

        last_line = int(self.text.index("end-1c").split(".")[0])
        width = len(str(last_line))

        for i in range(1, last_line + 1):
            self.line_numbers.insert("end", f"{str(i).rjust(width)}\n")

        self.line_numbers.configure(state="disabled")

    def see_end(self):
        """Scroll both text and line numbers to bottom."""
        self.text.see("end")
        self.line_numbers.yview_moveto(1.0)
