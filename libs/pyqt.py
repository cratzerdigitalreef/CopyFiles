# -*- coding: UTF-8 -*-

import sys
import os

#PYQT IMPORTS
#from PySide6.QtUiTools import QUiLoader
#from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QTextEdit, QFileDialog 
#from PySide6.QtCore import QFile, QIODevice

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtWidgets import QMessageBox, QTextEdit, QFileDialog, QTableView
from PyQt5.QtCore import QFile, QIODevice

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
       obj.setText(txt)

#---------------------------------------------------------------------------------------------------------
def pyqt_TextBoxGetText(obj):
    txt = ""
    if obj:   
       txt = obj.toPlainText(txt)
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
    if bDirOnly:
       option = QFileDialog.Option.ShowDirsOnly

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

       tReturn = filename[0]
       #print("tReturn length = " + str(len(tReturn)) + " - " + str(tReturn))

       if bDirOnly:
          n = 0
          tDirs = tReturn
          tReturn = []
          while n < len(tDirs):
                tDirs[n] = file_PathAndFile_GetPath(str(tDirs[n]))
                if not str(tDirs[n]) in str(tReturn):
                    tReturn.append(tDirs[n])
                n = n + 1
          #print("tReturn len = " + str(len(tReturn)) + " => " + str(tReturn))
       
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
    
