# -*- coding: UTF-8 -*-

import sys
import os

#PYQT IMPORTS
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtWidgets import QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QTextEdit, QFileDialog 
from PySide6.QtCore import QFile, QIODevice

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

    loader = QUiLoader()
    window = loader.load(ui_file)
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

    return len(tObjects)

#---------------------------------------------------------------------------------------------------------
def pyqt_TextEdit(txt, bReadOnly=True):
    if txt:
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
       obj.setText(txt)

#---------------------------------------------------------------------------------------------------------
def pyqt_TextBoxGetText(obj):
    txt = ""
    if obj:   
       txt = obj.toPlainText(txt)
    return txt   

#---------------------------------------------------------------------------------------------------------
def pyqt_OpenFileDlg(parent, sTitle, sPath, sFilters="All Files (*)"):
    # Open the file dialog
    # getOpenFileName returns a tuple: (filename, filter)

    if sFilters == "":
       sFilters = "All Files (*);;Text Files (*.txt);;"

    filename = QFileDialog.getOpenFileName(
                         parent,  # Parent widget
                         sTitle,  # Dialog title
                         sPath,  # Initial directory (empty string means current working directory)
                         sFilters  # File filters
                         )

    if filename:  # If a file was selected (not cancelled)
       return str(filename)
    else:
       return ""
    
#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxOk(parent, sHeader, sText):
    return pyqt_MsgBox(parent, sHeader, sText)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxYesNo(parent, sHeader, sText, bDefaultYes=True):
    bDef = QMessageBox.Yes
    if not bDefaultYes:
       bDef = QMessageBox.No

    return pyqt_MsgBox(parent, sHeader, sText, QMessageBox.Yes | QMessageBox.No, bDef)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxOkCancel(parent, sHeader, sText, bDefaultOk=True):
    bDef = QMessageBox.Ok
    if not bDefaultOk:
       bDef = QMessageBox.Cancel

    return pyqt_MsgBox(parent, sHeader, sText, QMessageBox.Ok | QMessageBox.Cancel, bDef)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBoxAbortRetryIgnore(parent, sHeader, sText, bDefaultAbort, bDefaultRetry, bDefaultIgnore):
    bDef = QMessageBox.Abort
    if not bDefaultRetry:
       bDef = QMessageBox.Retry
    if not bDefaultIgnore:
       bDef = QMessageBox.Ignore

    return pyqt_MsgBox(parent, sHeader, sText, QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore, bDef)

#---------------------------------------------------------------------------------------------------------
def pyqt_MsgBox(parent, sHeader, sText, btns=QMessageBox.Ok, btnDefault=QMessageBox.Ok):
    #https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
    if not btns:
       btns = QMessageBox.Ok

    if not btnDefault:   
       btnDefault = QMessageBox.Ok

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
    
