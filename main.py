#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(current+"/libs")

# LIBS
from log import * 
from str import *
from files import *

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current+"/constants")
sys.path.append(current+"/iu")

# CONSTANTS
from constants.general import *

from iu.copyfiles import CopyFilesHomeScreen


if __name__ == "__main__":

    str_client = app_name

    sPath = "D:\\Temp\\vbp\\NET\FilesCopy\\.vs\\FilesCopy\\v15"
    sPathInit = "D:\\Temp\\vbp\\NET"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

    sPath = "D:\\Temp\\vbp\\NET\\RunBATAsAdminTest\\RunBATAsAdminTest\\RunBATAsAdminTest\\RunBATAsAdminTest.vbproj.user"
    sPathInit = "D:\\Temp\\vbp\\NET"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

    sPath = "D:\\Temp\\vbp\\NET\\RunBATAsAdminTest\\RunBATAsAdminTest\\.vs\\RunBATAsAdminTest"
    sPathInit = "D:\\Temp\\vbp\\NET"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")
    
    sPath = "D:\\Temp\\vbp\\DLLs\\ADO\\Cls\\clsADO.cls"
    sPathInit = "D:\\Temp\\vbp"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

    sPath = "D:\\Temp\\vbp\\AgendaC\\vbp\\DLLs"
    sPathInit = "D:\\Temp\\vbp"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

    sPath = "D:\\Temp\\vbp\\NET\\FilesCopy"
    sPathInit = "D:\\Temp\\vbp\\NET"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

    sPath = "D:\\Temp\\vbp\\NET\\Class"
    sPathInit = "D:\\Temp\\vbp\\NET"
    sPathTo = "G:\\Temp"
    sPathToResult = files_CopyFiles_CopyFromTo_PreparePathTo(sPathTo, sPath, "", sPathInit)
    n = n + 1
    print("\n*** " + str(n) + " - sPathToResult: " + str(sPathToResult) + " - sPath: " + str(sPath) + " - sPathInit: " + str(sPathInit) + " - sPathTo: " + str(sPathTo) + "\n\n")

   
    exit(0)    

    current = os.path.dirname(os.path.realpath(__file__)) 
    str_log_file = log_setup_log_file(current, str_client)
    
    copyfiles = CopyFilesHomeScreen(str_client, str_log_file)

    
    #copyfiles.run()
    