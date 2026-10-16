# -*- coding: UTF-8 -*-

import sys
from str import *
from bytes import *
from files import *
from dt import *
from validanro import *
from log import *

ota_sDef_OTAScriptsName = "Applet"
ota_nDef_OTASMPPLength = 140
ota_sDef_OTAScriptsAmount = "10"
ota_sDef_FileNameSepara = "_"

ota_9000 = "9000"
ota_6101 = "6101"
ota_RPADU = "RAPDU"

ota_sDef_SIMSupplierThales = "Thales"
ota_sDef_SIMSupplierValid = "Valid"
ota_sDef_SIMSupplierGyD = "GyD"
ota_sDef_SIMSupplierIdemia = "Idemia"
ota_sDef_SIMSupplierWordCards = "WorldCards"
ota_sDef_SIMSupplierNXP = "NXP"
ota_sDef_SIMSupplierEaglefly = "Eaglefly"

ota_sDef_SIMSupplierValidGyDIdemia = ota_sDef_SIMSupplierValid + ota_sDef_SIMSupplierGyD + ota_sDef_SIMSupplierIdemia + ota_sDef_SIMSupplierWordCards + ota_sDef_SIMSupplierNXP + ota_sDef_SIMSupplierEaglefly
ota_sDef_SIMSupplierNoValidNoThales = ota_sDef_SIMSupplierGyD + ota_sDef_SIMSupplierIdemia + ota_sDef_SIMSupplierWordCards + ota_sDef_SIMSupplierNXP + ota_sDef_SIMSupplierEaglefly

ota_sDef_SIMSupplierValidGyDIdemia_9000 = ota_RPADU + ota_sDef_FileNameSepara + ota_9000 + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierGyD + ota_sDef_SIMSupplierIdemia + ota_sDef_SIMSupplierWordCards + ota_sDef_SIMSupplierNXP + ota_sDef_SIMSupplierEaglefly
ota_sDef_SIMSupplierValidGyDIdemia_6101 = ota_RPADU + ota_sDef_FileNameSepara + ota_6101 + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValid + ota_sDef_SIMSupplierGyD + ota_sDef_SIMSupplierIdemia + ota_sDef_SIMSupplierWordCards + ota_sDef_SIMSupplierNXP + ota_sDef_SIMSupplierEaglefly

ota_sDef_OTAExtThales = ".script"
ota_sDef_OTAExtValid = ".xml"

ota_sDef_OTAAdvanced = "OTAA"
ota_sDef_OTAClassic = "OTAClassic"

ota_sDef_OTAThalesScript = ota_sDef_SIMSupplierThales + "PlatformOTAScript"
ota_sDef_OTAValidScriptOTATool = ota_sDef_SIMSupplierValid + "PlatformOTAScript"
ota_sDef_OTAIdemiaScriptOTATool = ota_sDef_SIMSupplierIdemia + "PlatformOTAScript"
ota_sDef_OTAGyDScriptOTATool = ota_sDef_SIMSupplierGyD + "PlatformOTAScript"

#THALES PLATFORM SCRIPT CHARACTERS
ota_sDef_OTAThalesScript_Comment = "//"
ota_sDef_OTAThalesScript_CommentStart = "/*"
ota_sDef_OTAThalesScript_CommentFinish = "*/"
ota_nDef_OTAThalesScript_ByteStream = 0
ota_sDef_OTAValidScript_CommentStart = "<!-- "
ota_sDef_OTAValidScript_CommentFinish = " -->"
ota_sDef_OTAAThalesAPDUStart = "22"
ota_sDef_OTAClassicThalesAPDUStart = "write(" + str_GetComillaDoble() + "0x"
ota_sDef_OTAClassicThalesAPDUEnd = str_GetComillaDoble() + ");"
ota_sDef_OTAClassicValidAPDUStart = "<command>"
ota_sDef_OTAClassicValidAPDUEnd = "</command>"


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_OTAForDeletePackageAndInstance 
def ota_OTAForDeletePackageAndInstance(OTAScriptsName, sPathOut, sAIDPackage, sAPDUDelPackage, sAIDInstance, sAPDUDelInstance):

    sMsg = "Delete package and/or instance only. AID Package: " + str(sAIDPackage) + " - AID Instance: " + str(sAIDInstance) + "."
    log_writePrintOnlyDebug(sMsg)

    bReturn = True
    
    if OTAScriptsName == "":
       OTAScriptsName = ota_sDef_OTAScriptsName
   
    if sPathOut == "" or sAPDUDelPackage == "" or sAPDUDelInstance == "":
       return False
       
    sProcessFileRef = "OnlyDELETE"
    
    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sSIMSupplier = ota_sDef_SIMSupplierThales
    sExt = ota_sDef_OTAExtThales
    sProcessRef = "DeleteApplet"
    ota_ThalesOTAPlatformClassicByteStreamReset()
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAThalesScript
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES CLASSIC OTA
    # THALES
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAClassic
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformClassicHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Instance: " + sAIDInstance
       ota_ThalesOTAPlatformClassicAPDU(sAPDUDelInstance, sInfo, sFileNameProc)

       sInfo = "DELETE Package: " + sAIDPackage
       ota_ThalesOTAPlatformClassicAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_ThalesOTAPlatformClassicFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID, GyD e IDEMIA - CLASSIC OTA
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAClassic
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformClassicHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Package: " + sAIDPackage
       ota_ThalesOTAPlatformClassicAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_ThalesOTAPlatformClassicFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES ADVANCED OTA
    # THALES
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales + ota_RPADU + ota_9000
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())

    tOTAAdvanced = []
        
    if sFileNameProc != "":
 
       tOTAAdvanced.append(sAPDUDelInstance)
       tOTAAdvanced.append(sAPDUDelPackage)
       ota_ThalesOTAPlatformAdvancedAPDU(tOTAAdvanced, sFileNameProc)
       ota_ThalesOTAPlatformAdvancedFooter(2, sFileNameProc, ota_sDef_SIMSupplierThales)

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID - THALES ADVANCED OTA - RAPDU 6101
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia_6101
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())

    tOTAAdvanced = []
        
    if sFileNameProc != "":
 
      # tOTAAdvanced.append(sAPDUDelInstance) => NOT USED BECAUSE IT IS ONLY DELETED THE PACKAGE AND RELATIVES
       tOTAAdvanced.append(sAPDUDelPackage)
       ota_ThalesOTAPlatformAdvancedAPDU(tOTAAdvanced, sFileNameProc)
       ota_ThalesOTAPlatformAdvancedFooter(1, sFileNameProc, ota_sDef_SIMSupplierValidGyDIdemia)

    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA - GYD - ETC - ADVANCED THALES OTA - RAPDU 9000
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia_9000
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())

    tOTAAdvanced = []
        
    if sFileNameProc != "":
 
      # tOTAAdvanced.append(sAPDUDelInstance) => NOT USED BECAUSE IT IS ONLY DELETED THE PACKAGE AND RELATIVES
       tOTAAdvanced.append(sAPDUDelPackage)
       ota_ThalesOTAPlatformAdvancedAPDU(tOTAAdvanced, sFileNameProc)
       ota_ThalesOTAPlatformAdvancedFooter(1, sFileNameProc, ota_sDef_SIMSupplierNoValidNoThales)

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sSIMSupplier = ota_sDef_SIMSupplierThales
    sExt = ota_sDef_OTAExtValid
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAValidScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID CLASSIC OTA
    # THALES
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ValidOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Instance: " + sAIDInstance
       ota_ValidOTAPlatformAPDU(sAPDUDelInstance, sInfo, sFileNameProc)

       sInfo = "DELETE Package: " + sAIDPackage
       ota_ValidOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_ValidOTAPlatformFooter(sFileNameProc)
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID CLASSIC OTA
    # VALID, GyD, IDEMIA, Worldcards y NXP
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ValidOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Package: " + sAIDPackage
       ota_ValidOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_ValidOTAPlatformFooter(sFileNameProc)
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sSIMSupplier = ota_sDef_SIMSupplierThales
    sExt = ota_sDef_OTAExtValid
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAIdemiaScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA CLASSIC OTA
    # THALES
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_IdemiaOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Instance: " + sAIDInstance
       ota_IdemiaOTAPlatformAPDU(sAPDUDelInstance, sInfo, sFileNameProc)

       sInfo = "DELETE Package: " + sAIDPackage
       ota_IdemiaOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_IdemiaOTAPlatformFooter(sFileNameProc)
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA CLASSIC OTA
    # VALID, GyD, IDEMIA, Worldcards y NXP
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_IdemiaOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Package: " + sAIDPackage
       ota_IdemiaOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_IdemiaOTAPlatformFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------
    # GYD OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sSIMSupplier = ota_sDef_SIMSupplierThales
    sExt = ota_sDef_OTAExtThales
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAGyDScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # GYG CLASSIC OTA
    # THALES
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_GyDOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Instance: " + sAIDInstance
       ota_GyDOTAPlatformAPDU(sAPDUDelInstance, sInfo, sFileNameProc)

       sInfo = "DELETE Package: " + sAIDPackage
       ota_GyDOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_GyDOTAPlatformFooter(sFileNameProc)
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA CLASSIC OTA
    # VALID, GyD, IDEMIA, Worldcards y NXP
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_GyDOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       sInfo = "DELETE Package: " + sAIDPackage
       ota_GyDOTAPlatformAPDU(sAPDUDelPackage, sInfo, sFileNameProc)
       
       ota_GyDOTAPlatformFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------

    return bReturn    

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_OTAForLoadPackageAndInstallApplet 
def ota_OTAForLoadPackageAndInstallApplet(OTAScriptsName, sOTAScriptsAmount, sPathOut, sAIDPackage, sAIDInstance, lstAPDUs):

    bReturn = True

    if OTAScriptsName == "":
       OTAScriptsName = ota_sDef_OTAScriptsName
    if sOTAScriptsAmount == "":
       sOTAScriptsAmount = ota_sDef_OTAScriptsAmount

    if sPathOut == "" or len(lstAPDUs) <= 0:
       return False

    nOTAScriptsAmount = 10
    if not valid_nro_IsCharValidNro(sOTAScriptsAmount, True): 
       return False
    else:
       nOTAScriptsAmount = int(sOTAScriptsAmount)

    #RESET BYTSTREAM VARIABLE FOR TAHLES SCRIPTS
    ota_ThalesOTAPlatformClassicByteStreamReset()
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # INSTALL PACKAGE
    # -------------------------------------------------------------------------------------------------------------------------------
    
    nOTAClassicFiles = 0

    sFileNameProcOldThales = ""
    sFileNameProcThales = ""
    sFileNameProcOldValid = ""
    sFileNameProcValid = ""
    sFileNameProcOldIdemia = ""
    sFileNameProcIdemia = ""
    sFileNameProcOldGyD = ""
    sFileNameProcGyD = ""

    sProcessRef = "InstallApplet"
    
    sFileSplitFooterDes = ""
    nFileSplitAPDUsTogether = 0

    sSplitRef = "split"
    
    sFrom = ""
    nFrom = 0
    sTo = ""
    nTo = 0
    nTotalBytes = 0

    nTotalBytesAll = 0
    sFileNameProcAllThales = ""
    sFileNameProcAllValid = ""
    sFileNameProcAllIdemia = ""
    sFileNameProcAllGyD = ""
    sFileSplitFooterDesAll = ""

    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES OTA PLATFORM - COMPLETE
    # -------------------------------------------------------------------------------------------------------------------------------
    sFileNameThales = OTAScriptsName 
    sFileNameThales = sFileNameThales + ota_sDef_FileNameSepara + ota_sDef_OTAThalesScript

    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES CLASSIC OTA - COMPLETE - CLASSIC
    sFileNameProcThales = sFileNameThales
    sFileNameProcThales = sFileNameProcThales + ota_sDef_FileNameSepara + ota_sDef_OTAClassic
    sFileNameProcAllThales = sFileNameProcThales
    sFileNameProcAllThales = sFileNameProcAllThales + ota_sDef_OTAExtThales
    sFileNameProcAllThales = ota_FileCreate(sPathOut, sFileNameProcAllThales, ota_ThalesOTAPlatformClassicHeader(sProcessRef))

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID OTA PLATFORM - COMPLETE
    # -------------------------------------------------------------------------------------------------------------------------------
    sFileNameValid = OTAScriptsName 
    sFileNameValid = sFileNameValid + ota_sDef_FileNameSepara + ota_sDef_OTAValidScriptOTATool
    sFileNameProcAllValid = sFileNameValid
    sFileNameProcAllValid = sFileNameProcAllValid + ota_sDef_OTAExtValid
    sFileNameProcAllValid = ota_FileCreate(sPathOut, sFileNameProcAllValid, ota_ValidOTAPlatformHeader(sProcessRef))

    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA OTA PLATFORM - COMPLETE
    # -------------------------------------------------------------------------------------------------------------------------------
    sFileNameIdemia = OTAScriptsName 
    sFileNameIdemia = sFileNameIdemia + ota_sDef_FileNameSepara + ota_sDef_OTAIdemiaScriptOTATool
    sFileNameProcAllIdemia = sFileNameIdemia
    sFileNameProcAllIdemia = sFileNameProcAllIdemia + ota_sDef_OTAExtValid
    sFileNameProcAllIdemia = ota_FileCreate(sPathOut, sFileNameProcAllIdemia, ota_IdemiaOTAPlatformHeader(sProcessRef))

    # -------------------------------------------------------------------------------------------------------------------------------
    # GYD OTA PLATFORM - COMPLETE
    # -------------------------------------------------------------------------------------------------------------------------------
    sFileNameGyD = OTAScriptsName 
    sFileNameGyD = sFileNameGyD + ota_sDef_FileNameSepara + ota_sDef_OTAGyDScriptOTATool
    sFileNameProcAllGyD = sFileNameGyD
    sFileNameProcAllGyD = sFileNameProcAllGyD + ota_sDef_OTAExtThales
    sFileNameProcAllGyD = ota_FileCreate(sPathOut, sFileNameProcAllGyD, ota_GyDOTAPlatformHeader(sProcessRef))

    # -------------------------------------------------------------------------------------------------------------------------------
    n = 0 
    sFileNameProcThales = ""
    sFileNameProcValid = ""
    sFileNameProcIdemia = ""
    sFileNameProcGyD = ""
    
    while n < len(lstAPDUs) and bReturn:
    
          sMsg = "Load Package and Install Applet: processing APDU " + str(int(n+1)) + " from " + str(len(lstAPDUs)) + " ..."
          log_writePrintOnlyDebug(sMsg)
          
          lstAPDUs[n] = str_SpacesOut(lstAPDUs[n])
          sP1 = str_mid(lstAPDUs[n], 4, 2)
          sP2 = str_mid(lstAPDUs[n], 6, 2)

          if n == 0:
             # IT IS THE INSTALL FOR LOAD
             sInfo = "Install for Load - Package: " + sAIDPackage

          if n > 0 and n < (len(lstAPDUs)-1):
             # LOADING PACKAGE BLOCKS
             sInfo = "Load " + str(n-1) + " - Reference (P1 and P2): 0x" + sP1 + " " + sP2 + " (P2 0x" + sP2 + " in decimal: " + bytes_HexaToNro(sP2) + ")"

          if n == (len(lstAPDUs)-1):
             # THIS IS THE INSTALL FOR INSTALL
             sInfo = "Install for Install and Make Selectable - Package: " + sAIDPackage + " - Instance: " + sAIDInstance
          
          sTo = sInfo
          nTo = n
          
          if (n % nOTAScriptsAmount) == 0:
             #NEW FILE

             nOTAClassicFiles = nOTAClassicFiles + 1
             sFileNameProcOldThales = sFileNameProcThales
             sFileNameProcOldValid = sFileNameProcValid
             sFileNameProcOldIdemia = sFileNameProcIdemia
             sFileNameProcOldGyD = sFileNameProcGyD
             
             # -------------------------------------------------------------------------------------------------------------------------------
             # THALES OTA PLATFORM
             # -------------------------------------------------------------------------------------------------------------------------------
 
             # -------------------------------------------------------------------------------------------------------------------------------
             # THALES CLASSIC OTA
             sFileNameProcThales = sFileNameThales
             sFileNameProcThales = sFileNameProcThales + ota_sDef_FileNameSepara + ota_sDef_OTAClassic
             
             sFileNameProcThales = sFileNameProcThales + ota_sDef_FileNameSepara + sSplitRef + str(nOTAClassicFiles)
             sFileNameProcThales = sFileNameProcThales + ota_sDef_OTAExtThales
 
             sFileNameProcThales = ota_FileCreate(sPathOut, sFileNameProcThales, ota_ThalesOTAPlatformClassicHeader(sProcessRef))

             # -------------------------------------------------------------------------------------------------------------------------------
             # VALID OTA PLATFORM
             # -------------------------------------------------------------------------------------------------------------------------------
             sFileNameProcValid = sFileNameValid
             sFileNameProcValid = sFileNameProcValid + ota_sDef_FileNameSepara + sSplitRef + str(nOTAClassicFiles)
             sFileNameProcValid = sFileNameProcValid + ota_sDef_OTAExtValid

             sFileNameProcValid = ota_FileCreate(sPathOut, sFileNameProcValid, ota_ValidOTAPlatformHeader(sProcessRef))
    
             # -------------------------------------------------------------------------------------------------------------------------------
             # IDEMIA OTA PLATFORM
             # -------------------------------------------------------------------------------------------------------------------------------
             sFileNameProcIdemia = sFileNameIdemia
             sFileNameProcIdemia = sFileNameProcIdemia + ota_sDef_FileNameSepara + sSplitRef + str(nOTAClassicFiles)
             sFileNameProcIdemia = sFileNameProcIdemia + ota_sDef_OTAExtValid

             sFileNameProcIdemia = ota_FileCreate(sPathOut, sFileNameProcIdemia, ota_IdemiaOTAPlatformHeader(sProcessRef))

             # -------------------------------------------------------------------------------------------------------------------------------
             # GYD OTA PLATFORM
             # -------------------------------------------------------------------------------------------------------------------------------
             sFileNameProcGyD = sFileNameGyD
             sFileNameProcGyD = sFileNameProcGyD + ota_sDef_FileNameSepara + sSplitRef + str(nOTAClassicFiles)
             sFileNameProcGyD = sFileNameProcGyD + ota_sDef_OTAExtThales

             sFileNameProcGyD = ota_FileCreate(sPathOut, sFileNameProcGyD, ota_GyDOTAPlatformHeader(sProcessRef))

             # -------------------------------------------------------------------------------------------------------------------------------
             
             if sFileNameProcOldThales != "" and ota_sDef_OTAExtThales in sFileNameProcOldThales:
                sDes = "TOTAL COMMANDS TOGETHER: " + str(nTo - nFrom) + " - Number of SMPP for sending applet by SMS (estimation => total bytes " + str(nTotalBytes) + " / " + str(ota_nDef_OTASMPPLength) + " per SMPP): " + ota_OTAForLoadPackageAndInstallApplet_BytesTogether(nTotalBytes)
                sDes = sDes + "\n" + " - From Command '" + sFrom + "' To Command '" + sTo + "'"
                sDes = sDes + "\n" + sFileSplitFooterDes 

                ota_ThalesOTAPlatformClassicFooter(sFileNameProcOldThales, sDes)
                ota_ValidOTAPlatformFooter(sFileNameProcOldValid, sDes)
                ota_IdemiaOTAPlatformFooter(sFileNameProcOldIdemia, sDes)
                ota_GyDOTAPlatformFooter(sFileNameProcOldGyD, sDes)

             sFrom = sInfo       
             nFrom = n
             
             sFileSplitFooterDes = ""   
             nTotalBytes = 0
          
          # -------------------------------------------------------------------------------------------------------------------------------
          # THALES OTA PLATFORM - APDUs
          # -------------------------------------------------------------------------------------------------------------------------------
          #log_writePrintOnlyDebug("lstAPDUs => n = " + str(n) + " - lstAPDUs[n] = " + str(lstAPDUs[n]))
           
          ota_ThalesOTAPlatformClassicAPDU(lstAPDUs[n], sInfo, sFileNameProcThales)
          ota_ThalesOTAPlatformClassicAPDU(lstAPDUs[n], sInfo, sFileNameProcAllThales)

          # -------------------------------------------------------------------------------------------------------------------------------
          # VALID OTA PLATFORM - APDUs
          # -------------------------------------------------------------------------------------------------------------------------------
          ota_ValidOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcValid)
          ota_ValidOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcAllValid)

          # -------------------------------------------------------------------------------------------------------------------------------
          # IDEMIA OTA PLATFORM - APDUs
          # -------------------------------------------------------------------------------------------------------------------------------
          ota_IdemiaOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcIdemia)
          ota_IdemiaOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcAllIdemia)

          # -------------------------------------------------------------------------------------------------------------------------------
          # GYD OTA PLATFORM - APDUs
          # -------------------------------------------------------------------------------------------------------------------------------
          ota_GyDOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcGyD)
          ota_GyDOTAPlatformAPDU(lstAPDUs[n], sInfo, sFileNameProcAllGyD)

          # -------------------------------------------------------------------------------------------------------------------------------
          nTotalBytes = nTotalBytes + int(len(lstAPDUs[n])//2)
          nTotalBytesAll = nTotalBytesAll + int(len(lstAPDUs[n])//2)

          sFileSplitFooterDes = sFileSplitFooterDes + "\n" + str_SpaceHexa(lstAPDUs[n])
          sFileSplitFooterDesAll = sFileSplitFooterDesAll + "\n" + lstAPDUs[n]
                      
          n = n + 1   

    # -------------------------------------------------------------------------------------------------------------------------------
    
    if nTotalBytes > 0:
       sDes = "TOTAL COMMANDS TOGETHER: " + str(n - nFrom) + " - Number of SMPP for sending applet by SMS (estimation => total bytes " + str(nTotalBytes) + " / " + str(ota_nDef_OTASMPPLength) + " per SMPP): " + ota_OTAForLoadPackageAndInstallApplet_BytesTogether(nTotalBytes)
       sDes = sDes + "\n" + " - From Command '" + sFrom + "' To Command '" + sTo + "'"
       sDes = sDes + "\n" + sFileSplitFooterDes 
       ota_ThalesOTAPlatformClassicFooter(sFileNameProcThales, sDes)
       ota_ValidOTAPlatformFooter(sFileNameProcValid, sDes)
       ota_IdemiaOTAPlatformFooter(sFileNameProcIdemia, sDes)
       ota_GyDOTAPlatformFooter(sFileNameProcGyD, sDes)

    if nTotalBytesAll > 0:
       sDes = "ALL COMMANDS TOGETHER: " + str(len(lstAPDUs)) 
       sDes = sDes + "\nNumber of SMPP for sending applet by SMS (estimation => total bytes " + str(nTotalBytesAll) + " / " + str(ota_nDef_OTASMPPLength) + " per SMPP): " + ota_OTAForLoadPackageAndInstallApplet_BytesTogether(nTotalBytesAll)
       sDes = sDes + "\n" + sFileSplitFooterDesAll 
       ota_ThalesOTAPlatformClassicFooter(sFileNameProcAllThales, sDes)
       ota_ValidOTAPlatformFooter(sFileNameProcAllValid, sDes)
       ota_IdemiaOTAPlatformFooter(sFileNameProcAllIdemia, sDes)
       ota_GyDOTAPlatformFooter(sFileNameProcAllGyD, sDes)


    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES ADVANCED OTA
    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES
    sFileNameProc = sFileNameThales
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierThales + ota_RPADU + ota_9000
    sFileNameProc = sFileNameProc + ota_sDef_OTAExtThales
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())
    ota_ThalesOTAPlatformAdvancedAPDU(lstAPDUs, sFileNameProc)
    ota_ThalesOTAPlatformAdvancedFooter(len(lstAPDUs), sFileNameProc, ota_sDef_SIMSupplierThales)

    # -------------------------------------------------------------------------------------------------------------------------------
    # GyD, IDEMIA and Others - RAPDU 9000
    sFileNameProc = sFileNameThales
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia_9000
    sFileNameProc = sFileNameProc + ota_sDef_OTAExtThales
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())
    ota_ThalesOTAPlatformAdvancedAPDU(lstAPDUs, sFileNameProc)
    ota_ThalesOTAPlatformAdvancedFooter(len(lstAPDUs), sFileNameProc, ota_sDef_SIMSupplierNoValidNoThales)

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID, GyD e IDEMIA - RAPDU 6101
    sFileNameProc = sFileNameThales
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAAdvanced
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_SIMSupplierValidGyDIdemia_6101
    sFileNameProc = sFileNameProc + ota_sDef_OTAExtThales
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformAdvancedHeader())
    ota_ThalesOTAPlatformAdvancedAPDU(lstAPDUs, sFileNameProc)
    ota_ThalesOTAPlatformAdvancedFooter(len(lstAPDUs), sFileNameProc, ota_sDef_SIMSupplierValidGyDIdemia)


    # -------------------------------------------------------------------------------------------------------------------------------
    # INSTALL FOR INSTALL - ONLY 
    # -------------------------------------------------------------------------------------------------------------------------------
    bReturn = ota_OTAForInstallAppletOnly(OTAScriptsName, sPathOut, sAIDPackage, sAIDInstance, lstAPDUs)
    
    return bReturn    

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_OTAForLoadPackageAndInstallApplet_BytesTogether 
def ota_OTAForLoadPackageAndInstallApplet_BytesTogether(nBytes):
    
    nValFloat = float(nBytes/ota_nDef_OTASMPPLength)
    nVal = float(nBytes//ota_nDef_OTASMPPLength)
    
    #print("ota_OTAForLoadPackageAndInstallApplet_BytesTogether - nValFloat = " + str(nValFloat) + " - nVal = " + str(nVal))
    
    if nValFloat > nVal:
       nVal = nVal + 1

    #print("ota_OTAForLoadPackageAndInstallApplet_BytesTogether - nValFloat = " + str(nValFloat) + " - nVal = " + str(nVal))
    
    sVal = str(int(nVal))   
    if sVal == "0":
       sVal = "1"
    
    return sVal   

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_OTAForInstallAppletOnly 
def ota_OTAForInstallAppletOnly(OTAScriptsName, sPathOut, sAIDPackage, sAIDInstance, lstAPDUs):
       
    sMsg = "Install for install only. AID Package: " + str(sAIDPackage) + " - AID Instance: " + str(sAIDInstance) + "."
    log_writePrintOnlyDebug(sMsg)
   
    bReturn = True
    
    # -------------------------------------------------------------------------------------------------------------------------------
    # INSTALL FOR INSTALL - ONLY 
    # -------------------------------------------------------------------------------------------------------------------------------

    sProcessFileRef = "OnlyINSTALL FOR INSTALL"
    
    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sSIMSupplier = ota_sDef_SIMSupplierThales
    sExt = ota_sDef_OTAExtThales
    sProcessRef = "InstallApplet"
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAThalesScript
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # THALES CLASSIC OTA
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + ota_sDef_FileNameSepara + ota_sDef_OTAClassic
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ThalesOTAPlatformClassicHeader(sProcessRef))
    
    sAPDUInstallForInstall = lstAPDUs[len(lstAPDUs)-1]
    
    if sFileNameProc != "":

       sInfo = "Install for Install and Make Selectable - Package: " + sAIDPackage + " - Instance: " + sAIDInstance
       ota_ThalesOTAPlatformClassicAPDU(sAPDUInstallForInstall, sInfo, sFileNameProc)

       ota_ThalesOTAPlatformClassicFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sExt = ota_sDef_OTAExtValid
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAValidScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # VALID CLASSIC OTA
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_ValidOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       ota_ValidOTAPlatformAPDU(sAPDUInstallForInstall, sInfo, sFileNameProc)

       ota_ValidOTAPlatformFooter(sFileNameProc)
       
    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sExt = ota_sDef_OTAExtValid
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAIdemiaScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # IDEMIA CLASSIC OTA
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_IdemiaOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       ota_IdemiaOTAPlatformAPDU(sAPDUInstallForInstall, sInfo, sFileNameProc)

       ota_IdemiaOTAPlatformFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------
    # GYD OTA PLATFORM
    # -------------------------------------------------------------------------------------------------------------------------------
    sExt = ota_sDef_OTAExtThales
    
    sFileName = OTAScriptsName 
    sFileName = sFileName + ota_sDef_FileNameSepara + ota_sDef_OTAGyDScriptOTATool
    sFileName = sFileName + ota_sDef_FileNameSepara + sProcessFileRef

    # -------------------------------------------------------------------------------------------------------------------------------
    # GYD CLASSIC OTA
    sFileNameProc = sFileName
    sFileNameProc = sFileNameProc + sExt
    
    sFileNameProc = ota_FileCreate(sPathOut, sFileNameProc, ota_GyDOTAPlatformHeader(sProcessRef))
    
    if sFileNameProc != "":

       ota_GyDOTAPlatformAPDU(sAPDUInstallForInstall, sInfo, sFileNameProc)

       ota_GyDOTAPlatformFooter(sFileNameProc)

    # -------------------------------------------------------------------------------------------------------------------------------

    return bReturn    

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_CreateFile 
def ota_FileCreate(sPath, sFileName, sHeader):

    if str(sPath) == "" or str(sFileName) == "":
       sError = "File Creation ERROR. Path: " + str(sPath) + " and File Name: " + str(sFileName)
       log_writePrintOnlyError(sError)
       return False
       
    else:   
       try:
       
          print("ota_FileCreate - sPath: " + sPath)
          if not file_FileExists(sPath):
             os.mkdir(sPath)

          sPathFileName = os.path.join(sPath, sFileName)
        
          print("ota_FileCreate - sPathFileName: " + sPathFileName)

          file2write=open(sPathFileName,'w')
    
          if sHeader!="":
             file2write.write(sHeader)
    
          file2write.close()
          return sPathFileName

       except Exception as e:
          sError = "An unexpected error has occurred trying to create file: " + str(e)
          sError = sError + "\nPath: " + str(sPath) + " - File Name: " + str(sFileName) 
          log_writePrintOnlyError(sError)
          return ""

    return ""


# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformClassicHeader 
def ota_ThalesOTAPlatformClassicHeader(sProcess, sPathFileName=""):
    
    sRet = ota_sDef_OTAThalesScript_CommentStart
    sRet = sRet + "\nRAM TAR Applet = 00 00 00"
    sRet = sRet + "\n" + ota_sDef_OTAThalesScript_CommentFinish

    sRet = sRet + "\n\n" + "public class " + sProcess
    sRet = sRet + "\n" + "{"
    sRet = sRet + "\n" + "  public void script ()"
    sRet = sRet + "\n" + "  {"
    sRet = sRet + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)
       
    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformClassicFooter
def ota_ThalesOTAPlatformClassicFooter(sPathFileName="", sDataBeforeFooter=""):

    sRet = ""
    if sDataBeforeFooter != "":
       sRet = sRet + ota_sDef_OTAThalesScript_CommentStart
       sRet = sRet + "\n" + sDataBeforeFooter
       sRet = sRet + "\n" + ota_sDef_OTAThalesScript_CommentFinish
       sRet = sRet + "\n"
       
    sRet = sRet + "\n  }"
    sRet = sRet + "\n" + "}" + "\n"

    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)

    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformClassicAPDU 
def ota_ThalesOTAPlatformClassicAPDU(sAPDU, sRef, sPathFileName=""):

    sData = ""
    sAPDU = str_SpacesOut(sAPDU)
    
    sSpaces = str_RepeatString(8, " ")

    if sRef != "":
       sData = sData + sSpaces + ota_sDef_OTAThalesScript_Comment + sRef
    
    sByteStream = ota_ThalesOTAPlatformClassicByteStreamAdd()
    
    sData = sData + "\n" + sSpaces + "ByteStream "
    sData = sData + sByteStream
    sData = sData + " = new ByteStream();"
    
    sData = sData + "\n" + sSpaces
    sData = sData + sByteStream + ".write(" + str_GetComillaDoble() + "0x"
    sData = sData + sAPDU
    sData = sData + str_GetComillaDoble() + ");"

    sData = sData + "\n" + sSpaces + "passThrough(" + sByteStream + ".toByteArray());"
    sData = sData + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sData)

    return sData

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformClassicByteStreamAdd
def ota_ThalesOTAPlatformClassicByteStreamAdd():

   # GLOBAL VARIABLE TO SAVE LAST ENVELOPE SENT
   global ota_nDef_OTAThalesScript_ByteStream
   
   n = int(ota_nDef_OTAThalesScript_ByteStream)
   n = n + 1
   ota_nDef_OTAThalesScript_ByteStream = n
   
   sNewValue = ota_nDef_OTAThalesScript_ByteStream
   sNewValue = str_PaddingAddCharToTheRightByNro(5, str(sNewValue), "0", True)
   sNewValue = "s" + sNewValue
   
   #print("ota_ThalesOTAPlatformClassicByteStreamAdd - sNewValue = " + str(sNewValue))
   
   return sNewValue

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformClassicByteStreamReset
def ota_ThalesOTAPlatformClassicByteStreamReset():

   # GLOBAL VARIABLE TO SAVE LAST ENVELOPE SENT
   global ota_nDef_OTAThalesScript_ByteStream
   
   ota_nDef_OTAThalesScript_ByteStream = 0
   
   sNewValue = ota_nDef_OTAThalesScript_ByteStream
   sNewValue = str_PaddingAddCharToTheRightByNro(5, str(sNewValue), "0", True)
   sNewValue = "s" + sNewValue
   
   return sNewValue
   
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_FileWrite
def ota_FileWrite(sPathFileName, sData):

    if str(sPathFileName) != "" and sData != "":
 
       try:

          file2write=open(sPathFileName,'a')
          file2write.write(sData)
          file2write.close()
          return True
          
       except Exception as e:
          sError = "An unexpected error has occurred. " + str(e) 
          log_writePrintOnlyError(sError)
          return False
           
    else:
       sError = "File append ERROR. Path and File Name: " + str(sPathFileName) + " - Data: " + str(sData)
       log_writePrintOnlyError(sError)
       return False   

    return True

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformAdvancedHeader 
def ota_ThalesOTAPlatformAdvancedHeader(sPathFileName=""):
    
    sRet = "CAPDU (in):\n"
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)
       
    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformAdvancedFooter 
def ota_ThalesOTAPlatformAdvancedFooter(nCommands, sPathFileName="", sSIMSupplierRef=""):
    
    sRet = "RAPDU (out):\n"
    if sSIMSupplierRef != "":
       sRet = sRet + "(SIM Supplier = " + sSIMSupplierRef + ")\n"
    
    sPoR = "2302"
    
    sAOTA_RAPDU = ota_9000
    if sSIMSupplierRef != "":
        if ota_sDef_SIMSupplierValid.upper() in sSIMSupplierRef.upper():
           sAOTA_RAPDU = ota_6101
       
    if nCommands > 0:
       
       n = 0
       while n < nCommands:
       
             sRet = sRet + sPoR + sAOTA_RAPDU
                   
             n = n + 1
       
    sRet = sRet + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)

    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAPlatformAdvancedAPDU 
def ota_ThalesOTAPlatformAdvancedAPDU(tAPDU, sPathFileName=""):

    sData = ""
    
    sInit = ota_sDef_OTAAThalesAPDUStart
    
    if len(tAPDU)> 0:
    
       n = 0
       while n < len(tAPDU):
       
             sData = sData + sInit
             sAPDU = str_SpacesOut(tAPDU[n])
             
             nLen = int(len(sAPDU) // 2) 
             sLen = bytes_NroToHexa(nLen)
             
             sData = sData + sLen + sAPDU
             
             n = n + 1   
    
    sData = sData + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sData)

    return sData

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ValidOTAPlatformHeader 
def ota_ValidOTAPlatformHeader(sProcess, sPathFileName=""):
    
    today = datetime.now()
    today_prn = today.strftime("%Y/%m/%d %H:%M:%S")

    sSpaces = str_RepeatString(2, " ")

    sRet = "<?xml version=" + str_GetComillaDoble() + "1.0" + str_GetComillaDoble() + "?>"
    sRet = sRet + "\n<!DOCTYPE Session SYSTEM " + str_GetComillaDoble() + "scriptOta.dtd" + str_GetComillaDoble() + ">"
    sRet = sRet + "\n" + ota_sDef_OTAValidScript_CommentStart + "ScriptOTA - Remote Command session. Created on " + today_prn + ota_sDef_OTAValidScript_CommentFinish
    sRet = sRet + "\n<Session>"
    
    sRet = sRet + "\n" + sSpaces + "<settings commandType=" + str_GetComillaDoble() + "0" + str_GetComillaDoble()
    sRet = sRet + " tar=" + str_GetComillaDoble() + "000000" + str_GetComillaDoble()
    sRet = sRet + " counter=" + str_GetComillaDoble() + "0000000001" + str_GetComillaDoble()
    sRet = sRet + " kicKey=" + str_GetComillaDoble() + "11111111111111112222222222222222" + str_GetComillaDoble()
    sRet = sRet + " kidKey=" + str_GetComillaDoble() + "33333333333333334444444444444444" + str_GetComillaDoble()
    sRet = sRet + " spi=" + str_GetComillaDoble() + "02211515" + str_GetComillaDoble()
    sRet = sRet + " expanded=" + str_GetComillaDoble() + "False" + str_GetComillaDoble()
    sRet = sRet + " />"
    
    sRet = sRet + "\n" + sSpaces + "<smsPp udhi=" + str_GetComillaDoble() + "True" + str_GetComillaDoble()
    sRet = sRet + " rp=" + str_GetComillaDoble() + "False" + str_GetComillaDoble()
    sRet = sRet + " sri=" + str_GetComillaDoble() + "False" + str_GetComillaDoble() 
    sRet = sRet + " scts=" + str_GetComillaDoble() + "00000000000000" + str_GetComillaDoble()
    sRet = sRet + " oaToa=" + str_GetComillaDoble() + "81" + str_GetComillaDoble()
    sRet = sRet + " oa=" + str_GetComillaDoble() + "000000000000" + str_GetComillaDoble()
    sRet = sRet + " pid=" + str_GetComillaDoble() + "7F" + str_GetComillaDoble()
    sRet = sRet + " dcs=" + str_GetComillaDoble() + "F6" + str_GetComillaDoble()
    sRet = sRet + " scaToa=" + str_GetComillaDoble() + "81" + str_GetComillaDoble()
    sRet = sRet + " sca=" + str_GetComillaDoble() + "000000000000" + str_GetComillaDoble()
    sRet = sRet + " />"

    sRet = sRet + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)
       
    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ValidOTAPlatformFooter
def ota_ValidOTAPlatformFooter(sPathFileName="", sDesOptional=""):

    sSpaces = str_RepeatString(2, " ")

    sRet = ""
    if sDesOptional != "":
       sRet = sRet + sSpaces + ota_sDef_OTAValidScript_CommentStart
       sRet = sRet + "\n" + sDesOptional
       sRet = sRet + "\n" + ota_sDef_OTAValidScript_CommentFinish

    sRet = sRet + "\n</Session>"

    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)

    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ValidOTAPlatformAPDU 
def ota_ValidOTAPlatformAPDU(sAPDU, sRef, sPathFileName=""):

    sData = ""
    sAPDU = str_SpacesOut(sAPDU)

    sSpaces = str_RepeatString(2, " ")

    if sRef != "":
       sData = sData + sSpaces + ota_sDef_OTAValidScript_CommentStart + sRef + ota_sDef_OTAValidScript_CommentFinish
    
    sData = sData + "\n" + sSpaces + "<command>"
    sData = sData + str_SpaceHexa(sAPDU)
    sData = sData + "</command>"
    
    sData = sData + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sData)

    return sData

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ThalesOTAAScriptToAPDUList 
def ota_ThalesOTAAScriptToAPDUList(sScript, bShowResult=True, sLogPathFileOptional =""):

    sScript = str_SpacesOut(sScript)
    if str_left(sScript, 2) != ota_sDef_OTAAThalesAPDUStart:
       return sScript
    
    apdu = []

    n = 0
    while n < len(sScript):
          
          if str_mid(sScript, n, 2) == ota_sDef_OTAAThalesAPDUStart:
             n = n + 2
             sLen = str_mid(sScript, n, 2)
             n = n + 2
             nLen = int(int(bytes_HexaToNro(sLen)) * 2)
             sAPDU = str_mid(sScript, n, nLen)
             apdu.append(sAPDU)
             n = n + nLen
          else:   
             n = n + 2

    sPrint = "Total Thales Advanced OTA APDUs: " + str(len(apdu))
    n = 0
    while n < len(apdu):
          sPrint = sPrint + "\nAPDU nro " + str(n) + " from total " + str(len(apdu)) +  ": " + str(apdu[n])
          nBytes = int(len(apdu[n])/2)
          sPrint = sPrint + " - Length: " + str(len(apdu[n])) + " characters - (bytes = " + str(nBytes)
          #print("nBytes = " + str(nBytes))
          sPrint = sPrint + " - hexa = 0x" + bytes_NroToHexa(str(nBytes)) +  ")"
          n = n + 1

    if bShowResult:
       print(sPrint + "\n")

    if sLogPathFileOptional != "":
       log_write_Normal(sLogPathFileOptional, sPrint)

    return apdu
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_ScriptFileToAPDUs 
def ota_ScriptFileToAPDUs(sPathFile, sSeparaAPDU):

    sReturn = ""

    sData = fFileOpenTextModeAndRead(sPathFile)
    if sData == "":
       return sReturn

    #print("ota_ScriptFileToAPDUs - sData = " + sData)

    sExt = file_PathAndFile_GetFileNameExtension(sPathFile)
    sExt = str(sExt).upper()

    #print("ota_ScriptFileToAPDUs - sExt = " + sExt  + " from " + sPathFile)

    sSeparaAPDU = str(sSeparaAPDU)
    if sSeparaAPDU == "":
       sSeparaAPDU = ";"

    if sExt == "SCRIPT" or sExt == "XML":
       #THALES AND VALID OTA SCRIPTS
       lstData = sData.split("\n")

       #print("ota_ScriptFileToAPDUs - lstData = " + str(lstData) + " - Len: " + str(len(lstData)))

       if len(lstData) > 0:
          
          n = 0 
          while n < len(lstData):
                sLine = str_SpacesOut(lstData[n])
                n = n + 1

                if sLine == "":
                   continue
                
                #print("ota_ScriptFileToAPDUs - sLine = " + sLine)

                if sExt == "SCRIPT":
                   #THALES OTA SCRIPTS
                   #OTA ADVANCED
                   if str_left(sLine, 2) == ota_sDef_OTAAThalesAPDUStart:
                      sReturn = sReturn + sSeparaAPDU + sLine
                   else:
                      #OTA CLASSIC
                       if ota_sDef_OTAClassicThalesAPDUStart in sLine:
                          sReturnT = str_getSubStringFromOcur(sLine, ota_sDef_OTAClassicThalesAPDUStart, 1)
                          sReturnT = str_getSubStringFromOcur(sReturnT, ota_sDef_OTAClassicThalesAPDUEnd, 0)   
                          sReturn = sReturn + sSeparaAPDU + sReturnT

                   #print("ota_ScriptFileToAPDUs - n = " + str(n) + " - Thales - sReturn = " + sReturn)

                if sExt == "XML":   
                   #VALID OTA SCRIPTS
                   if ota_sDef_OTAClassicValidAPDUStart in sLine:
                          sReturnT = str_getSubStringFromOcur(sLine, ota_sDef_OTAClassicValidAPDUStart, 1)
                          sReturnT = str_getSubStringFromOcur(sReturnT, ota_sDef_OTAClassicValidAPDUEnd, 0)   
                          sReturn = sReturn + sSeparaAPDU + sReturnT

    if sReturn != "":
       
       if str_left(sReturn, len(sSeparaAPDU)) == sSeparaAPDU:
          sReturn = str_midToEnd(sReturn, len(sSeparaAPDU))

       #str_Replace(sReturn, sSeparaAPDU, sSeparaAPDU + str_GetENTER())   

       
    #print("ota_ScriptFileToAPDUs - sReturn = " + sLine)

    return sReturn   

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_IdemiaOTAPlatformHeader 
def ota_IdemiaOTAPlatformHeader(sProcess, sPathFileName=""):
    
    today = datetime.now()
    today_prn = today.strftime("%Y/%m/%d %H:%M:%S")

    sSpaces = str_RepeatString(2, " ")

    sRet = "<?xml version=" + str_GetComillaDoble() + "1.0 encoding=" + str_GetComillaDoble() + "UTF-8" + str_GetComillaDoble() + "?>"
    sRet = sRet + "\n" + ota_sDef_OTAValidScript_CommentStart + "ScriptOTA - Remote Command session. Created on " + today_prn + ota_sDef_OTAValidScript_CommentFinish
    sRet = sRet + "\n<AdminManagement Version=" + str_GetComillaDoble() + "1.0" + str_GetComillaDoble() + ">"
    
    sRet = sRet + "\n" + sSpaces + "<Job ID=" + str_GetComillaDoble() + "12345" + str_GetComillaDoble()
    #OLD
    #sRet = sRet + " TargetAID=" + str_GetComillaDoble() + "A000000003000000" + str_GetComillaDoble() + ">"
    #NEW
    sRet = sRet + " TargetAID=" + str_GetComillaDoble() + "A000000151000000" + str_GetComillaDoble() + ">"
    
    sRet = sRet + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)
       
    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_IdemiaOTAPlatformFooter
def ota_IdemiaOTAPlatformFooter(sPathFileName="", sDesOptional=""):

    sSpaces = str_RepeatString(2, " ")

    sRet = ""
    if sDesOptional != "":
       sRet = sRet + sSpaces + ota_sDef_OTAValidScript_CommentStart
       sRet = sRet + "\n" + sDesOptional
       sRet = sRet + "\n" + ota_sDef_OTAValidScript_CommentFinish

    sRet = sRet + "\n" + sSpaces + "</Job>"
    sRet = sRet + "\n</AdminManagement>"

    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)

    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_IdemiaOTAPlatformAPDU 
def ota_IdemiaOTAPlatformAPDU(sAPDU, sRef, sPathFileName=""):

    sData = ""
    sAPDU = str_SpacesOut(sAPDU)

    sSpaces = str_RepeatString(2, " ")

    if sRef != "":
       sData = sData + sSpaces + ota_sDef_OTAValidScript_CommentStart + sRef + ota_sDef_OTAValidScript_CommentFinish
    
    sData = sData + "\n" + sSpaces + "<Command"
    if sRef != "":
       sData = sData + " Name=" + str_GetComillaDoble() + sRef + str_GetComillaDoble()
    sData = sData + ">"
    sData = sData + "\n" + sSpaces + "<APDU>"
    sData = sData + str_SpaceHexa(sAPDU)
    sData = sData + "</APDU>"
    sData = sData + "\n" + sSpaces + "</Command>"
    
    sData = sData + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sData)

    return sData

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_GyDOTAPlatformHeader 
def ota_GyDOTAPlatformHeader(sProcess, sPathFileName=""):
    
    today = datetime.now()
    today_prn = today.strftime("%Y/%m/%d %H:%M:%S")

    sSpaces = str_RepeatString(2, " ")

    
    sRet = "# Select Security Domain (ISD)"
    sRet = sRet + "\n" + "A4 04 00 08 A0 00 00 01 51 00 00 00 (9000);"

    sRet = sRet + "\n\n" + "# Open Secure Channel"
    sRet = sRet + "\n" + "# INITIALIZE UPDATE and EXTERNAL AUTHENTICATE automatically, KEY_SET=1."
    sRet = sRet + "\n" + "SECURE_CHANNEL(LEVEL=ENC_AND_MAC, KEY_SET=1);"

    sRet = sRet + "\n\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)
       
    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_GyDOTAPlatformFooter
def ota_GyDOTAPlatformFooter(sPathFileName="", sDesOptional=""):

    sSpaces = str_RepeatString(2, " ")

    sRet = ""
    if sDesOptional != "":
       sRet = sRet + "\n#"
       
       sDesOptionalSplit = sDesOptional.split("\n")
       #print("ota_GyDOTAPlatformFooter - sDesOptionalSplit = " + str(len(sDesOptionalSplit)))

       sDesOptional = ""
       n = 0
       while n < len(sDesOptionalSplit):
          sDesOptional = sDesOptional + "\n# " + sDesOptionalSplit[n]
          n = n + 1

       sRet = sRet + sDesOptional + "\n"

    sRet = sRet + "\n" + "# Close session."
    sRet = sRet + "\n" + "EXIT;"

    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sRet)

    return sRet

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ota_GyDOTAPlatformAPDU 
def ota_GyDOTAPlatformAPDU(sAPDU, sRef, sPathFileName=""):

    sData = ""
    sAPDU = str_SpacesOut(sAPDU)

    sSpaces = str_RepeatString(2, " ")

    if sRef != "":
       sData = sData + "\n# " + sRef 
    
    sData = sData + "\n" + str_SpaceHexa(sAPDU)
    sData = sData + " (9000);"
    
    sData = sData + "\n"
    
    if str(sPathFileName) != "":
       ota_FileWrite(sPathFileName, sData)

    return sData

# --------------------------------------------------------------------------------------------------------------------------------------------------------
