# -*- coding: UTF-8 -*-

import sys
import os

#PYQT IMPORTS
#from PySide6.QtUiTools import QUiLoader
#from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QTextEdit, QFileDialog 
#from PySide6.QtCore import QFile, QIODevice

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView, QDesktopWidget, QAbstractItemView, QTreeView, QListView
from PyQt5.QtCore import QFile, QIODevice, Qt

from str import *
from bytes import *
from files import *
from pathlib import Path 
from log import *

#---------------------------------------------------------------------------------------------------------
def pyqt_open_ui_file(uiFilePathAndName):
    ui_file_name = uiFilePathAndName

    bReturn = True 
    print("ui_dile_name = " + ui_file_name)
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
       print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
       bReturn = False 

    #PySide6
    #loader = QUiLoader()
    #window = loader.load(ui_file)
    
    #PyQt5
    window = loadUi(ui_file)
       
    ui_file.close()
    if not window:
       print(loader.errorString())
       bReturn = False 
    
    return bReturn, window

#---------------------------------------------------------------------------------------------------------
def pyqt_getAllObjectsFromDialog(window):
    tObjects = window.children()
    n = 0
    while n < len(tObjects):
          print("pyqt_getAllObjectsFromDialog[" + str(n) + "] = " + str(tObjects[n]))
          n = n + 1
        
    return len(tObjects)

#---------------------------------------------------------------------------------------------------------
def pyqt_getAllObjectsFromMainWindow(main_window: QMainWindow):
    all_children = main_window.findChildren(QWidget)

    tObjects = []
    print("Children of the QMainWindow: " + str(main_window))
    n = 0
    for child in all_children:
        sChildType = str(type(child).__name__)
        if child.objectName():
            sObj = str(child.objectName()) + " - " 
        sObj = sObj + sChildType

        if sObj not in tObjects:
           tObjects.append(sObj)
           print("pyqt_getAllObjectsFromMainWindow[" + str(len(tObjects)-1) + "] = " + str(tObjects[len(tObjects)-1]))

        n = n + 1

    return tObjects

#---------------------------------------------------------------------------------------------------------
def pyqt_IsObjectInMainWindow(main_window: QMainWindow, objName):
    lst = pyqt_getAllObjectsFromMainWindow(QMainWindow)
    return pyqt_IsObjectInMainWindowList(lst, objName)

#---------------------------------------------------------------------------------------------------------
def pyqt_IsObjectInMainWindowList(lstQMainWindowObjList, objName):
    bReturn = False
    if len(lstQMainWindowObjList) > 0:
        if objName != "" and objName in str(lstQMainWindowObjList):
            bReturn = True

    return bReturn  

#---------------------------------------------------------------------------------------------------------
def pyqt_TextEditableReadOnly(txt, bReadOnly=True):
    #if txt:
    if bReadOnly:
       txt.setReadOnly(True)
    else:
       txt.setReadOnly(False)

#---------------------------------------------------------------------------------------------------------
def pyqt_EnableDisable(obj, bEnable=True):
    if obj:   
       obj.setEnabled(bEnable)

#---------------------------------------------------------------------------------------------------------
def pyqt_TextBoxSetText(obj, txt):
    if obj:   
       obj.setText(str(txt))

#---------------------------------------------------------------------------------------------------------
def pyqt_TextBoxGetText(obj):
    txt = ""
    if obj:   
       txt = obj.toPlainText()
    return txt   

#---------------------------------------------------------------------------------------------------------
def pyqt_ButtonSetText(obj, txt):
    if obj:   
       obj.setText(str(txt))

#---------------------------------------------------------------------------------------------------------
def pyqt_ButtonGetText(obj):
    txt = ""
    if obj:   
       txt = obj.text()
    return txt   

#---------------------------------------------------------------------------------------------------------
def pyqt_OpenFileDlgForSave(parent, sTitle, sPath, sFilters="All Files (*)", bDirOnly=False):
    return pyqt_OpenFileDlg(parent, sTitle, sPath, sFilters, bDirOnly, True, False)

#---------------------------------------------------------------------------------------------------------
def pyqt_OpenFileDlgDirOnly(parent, sTitle, sPath, sFilters="All Files (*)", bMoreFiles=False):
    #print("sFilters = " + str(sFilters))
    return pyqt_OpenFileDlg(parent, sTitle, sPath, sFilters, True, False, bMoreFiles)

#---------------------------------------------------------------------------------------------------------
def pyqt_OpenFileDlgMoreFiles(parent, sTitle, sPath, sFilters="All Files (*)"):
    return pyqt_OpenFileDlg(parent, sTitle, sPath, sFilters, False, False, True)

#---------------------------------------------------------------------------------------------------------
# IT IS ALWAYS RETURNED A LIST WITH SELECTED FILES/DIRS
# IF NOTHING IS SELECTED, THE LIST IS EMPTY WITH []
def pyqt_OpenFileDlg(parent, sTitle, sPath, sFilters="All Files (*)", bDirOnly=False, bSave=False, bMoreFiles=False):
    # Open the file dialog
    # getOpenFileName returns a tuple: (filename, filter)

    if sFilters == "":
       sFilters = "All Files (*);;"
       if not bDirOnly:
          sFilters = sFilters + "Text Files (*.txt);;"

    lstFiltes = sFilters.split(";;")
    sFiltersDefault = str(lstFiltes[0])

    #print("pyqt_OpenFileDlg - sFilters = " + str(sFilters) + " - bDirOnly = " + str(bDirOnly) + " - bMoreFiles = " + str(bMoreFiles))
    #print("pyqt_OpenFileDlg - sPath = " + str(sPath))

    option = 0

    if bSave:
       if option == 0:
          filename = QFileDialog.getSaveFileName(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault
                  )
       else:
          filename = QFileDialog.getSaveFileName(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault,
                         options=option #Options
                  )
    else:
       if bDirOnly:
          #option = QFileDialog.Option.ShowDirsOnly
          option = QFileDialog.Options()
          option |= QFileDialog.DontUseNativeDialog
          option |= QFileDialog.ShowDirsOnly  # This will now be effective

          if bMoreFiles:
              
              file_dialog = QFileDialog()
              file_dialog.setFileMode(QFileDialog.DirectoryOnly)
              file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
              #file_dialog.setParent(parent)
              file_dialog.setWindowTitle(sTitle)
              file_dialog.setDirectory(sPath)

              file_view = file_dialog.findChild(QListView, 'listView')

              # to make it possible to select multiple directories:
              if file_view:
                 file_view.setSelectionMode(QAbstractItemView.MultiSelection)

              f_tree_view = file_dialog.findChild(QTreeView)
              if f_tree_view:
                 f_tree_view.setSelectionMode(QAbstractItemView.MultiSelection)

              if file_dialog.exec():
                 filename = file_dialog.selectedFiles()

          else:            
                filename = QFileDialog.getExistingDirectory(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         options=option #Options
                )
           
       else:        
          if bMoreFiles:
             if option == 0:
                filename = QFileDialog.getOpenFileNames(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault
                  )
             else:
                filename = QFileDialog.getOpenFileNames(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault,
                         options=option #Options
                  )
          else:   
             if option == 0:
                filename = QFileDialog.getOpenFileName(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault
                  )
             else:
                filename = QFileDialog.getOpenFileName(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters,  # File filters
                         sFiltersDefault,
                         options=option #Options
                  )


    tReturn = []

    if filename:  # If a file was selected (not cancelled)

       #print("filename = " + str(filename))
       
       tReturn = filename[0]
       #print("tReturn length = " + str(len(tReturn)) + " - " + str(tReturn))

       if bDirOnly:
          #n = 0
          #tDirs = tReturn
          #tReturn = []
          #while n < len(tDirs):
          #      tDirs[n] = file_PathAndFile_GetPath(str(tDirs[n]))
          #      if not str(tDirs[n]) in str(tReturn):
          #          tReturn.append(tDirs[n])
          #      n = n + 1
          #print("tReturn len = " + str(len(tReturn)) + " => " + str(tReturn))
          tReturn = filename
        
    return tReturn
    
#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxOk(parent, sHeader, sText):
    return pyqt_MsgBoxQuestion(parent, sHeader, sText)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxYesNo(parent, sHeader, sText, bDefaultYes=True):
    bDef = QMessageBox.Yes
    if not bDefaultYes:
       bDef = QMessageBox.No

    tReturn = pyqt_MsgBoxQuestion(parent, sHeader, sText, QMessageBox.Yes | QMessageBox.No, bDef)

    #print("pyqt_MsgBoxYesNo - tReturn = " + str(tReturn))

    sReturn = "Yes"
    bReturn = True
    if tReturn == QMessageBox.StandardButton.No:
        sReturn = "No"
        bReturn = False
    
    return sReturn, bReturn

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxOkCancel(parent, sHeader, sText, bDefaultOk=True):
    bDef = QMessageBox.Ok
    if not bDefaultOk:
       bDef = QMessageBox.Cancel

    tReturn = pyqt_MsgBoxQuestion(parent, sHeader, sText, QMessageBox.Ok | QMessageBox.Cancel, bDef)

    sReturn = "Ok"
    bReturn = True
    if tReturn == QMessageBox.StandardButton.Cancel:
        sReturn = "Cancel"
        bReturn = False
    
    return sReturn, bReturn

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxAbortRetryIgnore(parent, sHeader, sText, bDefaultAbort, bDefaultRetry, bDefaultIgnore):
    bDef = QMessageBox.Abort
    if not bDefaultRetry:
       bDef = QMessageBox.Retry
    if not bDefaultIgnore:
       bDef = QMessageBox.Ignore

    tReturn = pyqt_MsgBoxQuestion(parent, sHeader, sText, QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore, bDef)

    sReturn = "Abort"
    if tReturn == QMessageBox.StandardButton.Retry:
        sReturn = "Retry"
    if tReturn == QMessageBox.StandardButton.Ignore:
        sReturn =  "Ignore"
    
    return sReturn

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxQuestionWithoutParent(sHeader, sText, btns=QMessageBox.Ok, btnDefault=QMessageBox.StandardButton.Ok):
    return pyqt_MsgBoxQuestion(None, sHeader, sText, btns, btnDefault)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxQuestion(parent, sHeader, sText, btns=QMessageBox.Ok, btnDefault=QMessageBox.StandardButton.Ok):
    #https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
    if not btns:
       btns = QMessageBox.StandardButton.Ok

    if not btnDefault:   
       btnDefault = QMessageBox.StandardButton.Ok

    #print("pyqt_MsgBox - parent = " + str(parent))
    #print("pyqt_MsgBox - sHeader = " + str(sHeader))
    #print("pyqt_MsgBox - sText = " + str(sText))
    #print("pyqt_MsgBox - btns = " + str(btns))
    #print("pyqt_MsgBox - btnDefault = " + str(btnDefault))

    #List of standard buttons to be displayed. Each button is associated with
    #QMessageBox.Ok 0x00000400
    #QMessageBox.Open 0x00002000
    #QMessageBox.Save 0x00000800
    #QMessageBox.Cancel 0x00400000
    #QMessageBox.Close 0x00200000
    #QMessageBox.Yes 0x00004000
    #QMessageBox.No 0x00010000
    #QMessageBox.Abort 0x00040000
    #QMessageBox.Retry 0x00080000
    #QMessageBox.Ignore 0x00100000

    reply = QMessageBox.question(parent, sHeader, sText, btns, btnDefault)

    return reply

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBox_Info(sHeader, sText, icon=QMessageBox.Icon.Information):
    return pyqt_MsgBox(sHeader, sText)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBox_Warning(sHeader, sText):
    return pyqt_MsgBox(sHeader, sText, QMessageBox.Icon.Warning)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBox_Error(sHeader, sText):
    return pyqt_MsgBox(sHeader, sText, icon=QMessageBox.Icon.Critical)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBox(sHeader, sText, icon=QMessageBox.Icon.Information):
    #https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
    
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(sText)
    msg.setWindowTitle(sHeader)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    retval = msg.exec()

    return retval

#---------------------------------------------------------------------------------------------------------
# CLASS QTextEdit for mapper events such as Double Click
#---------------------------------------------------------------------------------------------------------
class customPyQt_TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            
            #print("customPyQt_TextEdit - QTextEdit double-clicked!")
            
            sDes = self.toPlainText()
            if sDes !="":   
               print("customPyQt_TextEdit - sDes = " + sDes)

               if file_FileExists(sDes):
                   file_OpenFileWithNotepadInWindows(sDes)
               else:    
                   file_OpenNotePadInWindows(sDes)
            else:
                print("customPyQt_TextEdit - Nothing to show!")   
       
            # You can add your custom logic here
            # For example, select the entire word at the cursor
            # self.selectAll() 
            # Or perform some other action

        # Call the base class implementation to maintain default behavior
        super().mouseDoubleClickEvent(event)

#---------------------------------------------------------------------------------------------------------
# pyqt_windowRefresh
#---------------------------------------------------------------------------------------------------------
def pyqt_windowRefresh(mnWindow):
    try:
       mnWindow.update()
       return True, ""
    except Exception as e:
       sError = "ERROR for 'update' windows object '" + str(mnWindow) + ". ERROR: " + str(e)
       print(sError)
       return False, sError


#---------------------------------------------------------------------------------------------------------
# pyqt_centerWindow
#---------------------------------------------------------------------------------------------------------
def pyqt_centerWindow(window):
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()
        
        # Get the window geometry
        window_geometry = window.frameGeometry()
        
        # Calculate the center point of the screen
        center_point = screen.center()
        
        # Move the window's center to the screen's center
        window_geometry.moveCenter(center_point)
        
        # Apply the new geometry to the window
        window.setGeometry(window_geometry)
        
        return

#---------------------------------------------------------------------------------------------------------
# LoadingDialog
#---------------------------------------------------------------------------------------------------------
class LoadingDialog(QDialog):
    """
    A simple modal dialog designed to block user interaction while a background
    task is processing.

    This dialog displays a status message and optionally provides a 'Cancel'
    button if a callback is supplied.

    Attributes:
        message_label (QLabel): The label displaying the body text/status.
        cancel_button (QPushButton): The button created only if a cancel_callback
                                     is provided.
    """

    def __init__(self, title_text: str = "Loading", content_text: str = "Please wait...", cancel_callback=None):
        """
        Initialize the loading dialog.

        Args:
            title_text (str, optional): The text to display in the window title bar.
                                        Defaults to "Loading".
            content_text (str, optional): The initial message body text.
                                          Defaults to "Please wait...".
            cancel_callback (callable, optional): A function or method to be connected
                                                  to the Cancel button's clicked signal.
                                                  If None, no Cancel button is shown.
        """
        super().__init__()
        self.setWindowTitle(title_text)
        self.setModal(True)
        self.setFixedSize(200, 100)

        # CustomizeWindowHint and WindowTitleHint keep the title bar but often
        # remove the "X" close button depending on the OS/Window Manager.
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.message_label: QLabel = QLabel(content_text)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 16px;")

        layout.addWidget(self.message_label)

        if cancel_callback:
            self.cancel_button: QPushButton = QPushButton("Cancel")
            self.cancel_button.clicked.connect(cancel_callback)
            layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def update_text(self, text: str):
        """
        Updates the message displayed in the center of the dialog.

        Args:
            text (str): The new message string to display.
        """
        self.message_label.setText(text)

    def update_title(self, title: str):
        """
        Updates the text in the window's title bar.

        Args:
            title (str): The new title string to set.
        """
        self.setWindowTitle(title)

#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
    
