# -*- coding: UTF-8 -*-

import os
import colorama
from colorama import Fore  #(Se sugiere no usar versión superior a 0.4.5)
from datetime import *
from str import *
from prettytable import PrettyTable
import subprocess
import platform
import multiprocessing


#Defining the print types
dic_colorlog = {
                 'warning' : 'YELLOW' 
                ,'error' : 'RED'
                ,'success' : 'GREEN'
                ,'info' : 'CYAN'
                ,'debug' : 'MAGENTA'
                }

nValue = float(0)

# log_create ----------------------------------------------------------------------------------------------------------
def log_create(sPath, sFileName, sProcess = "", bAppend = False,sVerbose=True):
    return log_create_WithPath(sPath, sFileName, sProcess, bAppend,sVerbose)

# log_create_path ----------------------------------------------------------------------------------------------------------
def log_create_path(sPath):
    parent_directory = os.path.dirname(sPath)
    log_basename=os.path.basename(sPath)

    sDirLog = "logs_" + log_basename

    if not os.path.exists(os.path.join(sPath,sDirLog)):
        os.mkdir(os.path.join(sPath,sDirLog))
    
    return log_join_path_file(sPath, sDirLog)

# log_join_path_file ----------------------------------------------------------------------------------------------------------
def log_join_path_file(sPath, sFile):
    return os.path.join(sPath, sFile)

# log_create_WithPath ----------------------------------------------------------------------------------------------------------
def log_create_WithPath(sPath, sFileName, sProcess, bAppend, sVerbose=True):
    #Create directory in case that not exists
    log_basename=os.path.basename(sPath)
    if not os.path.exists(os.path.join(sPath,"logs_"+log_basename)):
        os.mkdir(os.path.join(sPath,"logs_"+log_basename))

    today = datetime.now()
    today_f = today.strftime("%Y-%m-%d")
    today_prn = today.strftime("%Y-%m-%d %H:%M:%S")
    sFileOut = os.path.join(sPath,"logs_"+log_basename,sFileName + "_" + str(today_f) + ".txt")
    
    sMode = "w"
    if bAppend == True:
       sMode = "a"
   
    file2write=open(sFileOut, sMode)

    sLog = str_RepeatString(100, "-")
    log_write(sFileOut, sLog)

    
    if sProcess != "":
       log_write(sFileOut, "PROCESS " + sProcess + ". STARTED: " + str(today_prn),sVerbose=sVerbose)
    file2write.close()

    sLog = str_RepeatString(100, "-")
    log_write(sFileOut, sLog,sVerbose=sVerbose)

    return sFileOut
  
# log_writeWithLineNro ----------------------------------------------------------------------------------------------------------
def log_writeWithLineNro(sFileName, sData, bPrint):
    file2write=open(sFileName, 'a')
    sLine = ""
    if nNroLine > 0:
       #sNroLine = '{:0>10}'.format(nNroLine)
       sNroLine = str_formatNro(nNroLine, 10) 
       today = datetime.now()
       today_prn = today.strftime("%Y-%m-%d %H.%M.%S")
       sLine = str(sNroLine) + " " + str(today_prn) + ": "
       
    sLine = sLine + sData
    file2write.write(sLine + "\n")
    if bPrint == True:
       print(sLine)
    file2write.close()
    return nNroLine + 1    

# log_writeLine ----------------------------------------------------------------------------------------------------------
def log_writeLine(sFileName, sData, bPrint):
    log_writeWithLineNro(sFileName, sData, 0, bPrint)


# log_write_Normal ----------------------------------------------------------------------------------------------------------
def log_write_Normal(sFileName, sData):
    log_write(sFileName, sData,sType='Normal')
# log_write_InfoInBlue ----------------------------------------------------------------------------------------------------------
def log_write_InfoInBlue(sFileName, sData):
    log_write(sFileName, sData, sType='info')
# log_write_ErrorInRed ----------------------------------------------------------------------------------------------------------
def log_write_ErrorInRed(sFileName, sData):
    log_write(sFileName, sData, sType='error')
def log_write_OKInGreen(sFileName, sData):
    log_write(sFileName, sData, sType='success')
def log_write_WarningInYellow(sFileName, sData):
    log_write(sFileName, sData, sType='warning')

    
# log_write ----------------------------------------------------------------------------------------------------------
def log_write(sFileName, sData, sType='Normal', sVerbose = True, bDate = True):
    """
    To color, add the variable 'sType'\n
    Example:\n
    sType = 'info' => Blue\n
    sType = 'warning' => Orange\n
    sType = 'error' => Red\n
    sType = 'ok' => Green\n
    """
    log_writeWithDateTime(sFileName, sData, sVerbose, sType, bDate)

# log_writeNoPrint ----------------------------------------------------------------------------------------------------------
def log_writeNoPrint(sFileName, sData):
    log_writeWithDateTime(sFileName, sData, False)

# log_writeWithDateTime ----------------------------------------------------------------------------------------------------------
def log_writeWithDateTime(sFileName, sData, bPrint, sType, bDate):

    sLine = ""

    if bDate:
        today = datetime.now()
        today_prn = today.strftime("%Y-%m-%d %H.%M.%S")
        today_prn = str(today_prn)
        sLine = today_prn + ": " 
       
    sLine = sLine + sData
    sLine = str_CleanNotPrintableASCII(sLine, "_")
    
    if sFileName!= "":
       file2write=open(sFileName, 'a')
       file2write.write(sLine + "\n")
    
    if bPrint:
       log_writeWordsInColor(sLine, sType)
    file2write.close()
    return sLine    

# log_writePrintOnlyInfo ----------------------------------------------------------------------------------------------------------
def log_writePrintOnlyInfo(sData):
    log_writeWordsInColorBlue(sData)
# log_writeWordsInColorBlue ----------------------------------------------------------------------------------------------------------
def log_writeWordsInColorBlue(sData):
    log_writeWordsInColor(sData, sType='info')
    
# log_writePrintOnlyWarning ----------------------------------------------------------------------------------------------------------
def log_writePrintOnlyWarning(sData):
    log_writeWordsInColorYellow(sData)
# log_writeWordsInColorYellow ----------------------------------------------------------------------------------------------------------
def log_writeWordsInColorYellow(sData):
    log_writeWordsInColor(sData, sType='warning')
    
# log_writePrintOnlyOK ----------------------------------------------------------------------------------------------------------
def log_writePrintOnlyOK(sData):
    log_writeWordsInColorGreen(sData)
# log_writeWordsInColorGreen ----------------------------------------------------------------------------------------------------------
def log_writeWordsInColorGreen(sData):
    log_writeWordsInColor(sData, sType='success')

# log_writePrintOnlyError ----------------------------------------------------------------------------------------------------------
def log_writePrintOnlyError(sData):
    log_writeWordsInColorRed(sData)
# log_writeWordsInColorRed ----------------------------------------------------------------------------------------------------------
def log_writeWordsInColorRed(sData):
    log_writeWordsInColor(sData, sType='error')

# log_writePrintOnlyDebug ----------------------------------------------------------------------------------------------------------
def log_writePrintOnlyDebug(sData):
    log_writeWordsInColorMagenta(sData)
def log_writeWordsInColorMagenta(sData):
    log_writeWordsInColor(sData, sType='debug')

# log_writeWordsInColor ----------------------------------------------------------------------------------------------------------
def log_writeWordsInColor(sData, sType='info'):
    # Refresh color
    #print("sType: " + str(sType))
    colorama.init(autoreset=True, strip=False)
    if sType in dic_colorlog:
       sColor = dic_colorlog.get(sType)
       #print("sType: " + str(sType))
       print(getattr(Fore, sColor)+ sData)
    else:
       print(sData)
    colorama.deinit()

    
# log_FileAppend ----------------------------------------------------------------------------------------------------------
def log_FileAppend(sFileName, sData):
    return log_SaveDataToFile(sFileName, sData, True)
    
# log_FileCreate ----------------------------------------------------------------------------------------------------------
def log_FileCreate(sFileName, sData):
    return log_SaveDataToFile(sFileName, sData, False)

# log_SaveDataToFile ----------------------------------------------------------------------------------------------------------
def log_SaveDataToFile(sFileName, sData, bAppend):
    
    sFlag = 'w'
    if bAppend:
       sFlag = 'a'
    
    file2write=open(sFileName,sFlag)
    
    if sData!="":
       file2write.write(sData)
    
    file2write.close()

    return file2write


# log_setup_log_file ----------------------------------------------------------------------------------------------------------
def log_setup_log_file(current_directory, client):
    log_file_name = log_create(current_directory, f"{client}",
                               f"APDU Commands - Client: {client}", True)
    return log_file_name


# Log print any dictionary ----------------------------------------------------------------------------------------------------------
def log_print_dict(log_file_name, obj):
    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = list(obj.keys())
    row_values = list(obj.values())

    table.add_row(row_values)

    # Convert the table to a string
    table_str = table.get_string()

    # Print the table to the log file
    log_write(log_file_name, "\n" + table_str + "\n", bDate=False)


# log_init_summary_terminal ----------------------------------------------------------------------------------------------------------
progress_log_queue = multiprocessing.Queue()
def log_init_summary_terminal(log_progress_with_path):
    """
    Method to initialize Process(thread) to start the new terminal where the progress will be displayed.

    To insert a progress message, you must import the progress_log_queue variable, as follows:
    
    from log import progress_log_queue
    
    Insert progress messages example:
        >>> progress_log_queue.put(log_progress)
    
    Stop inserting progress messages
        >>> progress_log_queue.put("STOP")

    Args:
        log_progress_with_path (str): a string with the path + file.txt that the terminal will be listening for

    Returns:
        Process (multiprocessing.Process): the process (thread) in which the terminal will run
        
        Terminal progress (subprocess.Popen): The terminal instance that opens

    Example:
        >>> printer_progress = log_init_summary_terminal(log_progress_with_path) 
    """
    # To open a terminal that shows the process status
    # progress_log_queue = multiprocessing.Queue()
    printer_process = multiprocessing.Process(target=__log_write_progress, args=(progress_log_queue,log_progress_with_path))
    printer_process.start()
    terminal_progress = __log_open_terminal(log_progress_with_path)
    return printer_process, terminal_progress


# log_print_progress ----------------------------------------------------------------------------------------------------------
def __log_write_progress(queue, log_progress_with_path):
    """
    Method that must be invoked with a thread (subprocess).
    It listens to a queue and writes information to the temporary file log_progress.txt 
    if there is new information.
    """
    while True:
       msg = queue.get()

       if msg.upper() == "STOP":
           break

        # Open the file in 'w' mode each time, so that the content is overwritten
       with open(log_progress_with_path, "w", encoding="utf-8") as log_file:
          log_file.write(msg + "\n")
          log_file.flush()


# log_open_terminal ----------------------------------------------------------------------------------------------------------
def __log_open_terminal(log_progress_with_path, refresh_rate = 500):
    """
    Opens a new terminal that, in a loop, clears the screen and displays 
    the updated content of temporal file log_progress.txt. 
    """
    if platform.system() == "Windows":
        # On Windows, we use a PowerShell loop to clear the screen and read the file every 500ms.
        ps_command = f"while ($true) {{ cls; Get-Content '{log_progress_with_path}'; Start-Sleep -Milliseconds {refresh_rate} }}"
        # Pasamos los argumentos en una lista para evitar problemas con escapes
        args = ["powershell.exe", "-NoExit", "-Command", ps_command]        
        terminal_progress = subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # On Linux, we use a bash loop to do the same.
        subprocess.Popen([r"x-terminal-emulator", "-e", "bash", "-c", "while true; do clear; cat \\'{self.log_progress_with_path}\\'; sleep 0.5; done"])
    return terminal_progress

