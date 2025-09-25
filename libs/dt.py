# -*- coding: UTF-8 -*-

from datetime import datetime
from datetime import timedelta

# for timezone()
import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

from str import *

# dt_now ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_now(sFormat):
    if str(sFormat)=="":
       sFormat = "%d/%m/%Y-%H:%M:%S"
    
    dateStart = datetime.now()    
    return dateStart.strftime(sFormat)
    
# dt_difference_sec ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference_sec(dtStart, dtEnd):
    dt = dtStart - dtEnd
    return str(dt.total_seconds())

# dt_difference ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference(sdtFormat, dtStart, dtEnd, bReturnCompleteMsg):
    
    sF = ".%f"
    if str_right(sdtFormat, len(sF)) != sF and str_instrBool(str(dtStart), "."):
       sdtFormat = sdtFormat + sF

    #print("dt_difference - Start: " + str(dtStart))
    #print("dt_difference - End: " + str(dtEnd))
    #print("dt_difference - sdtFormat: " + str(sdtFormat))
       
    #sFormatDT = "%d/%m/%Y-%H:%M:%S"
    #sFormatDT = "%Y%m%d%H%M%S"
    dtStart = datetime.strptime(str(dtStart),sdtFormat)
    dtEnd = datetime.strptime(str(dtEnd),sdtFormat)
    
    dt = dtEnd - dtStart
    sdt = str(dt)
    
    # Example 1: dt: 1 day, 13:52:01
    # Example 2: dt: 0:00:00.066847
    #print("dt: " + sdt)

    # GET DAYS
    nday = "0"
    sTemp = str_getSubStringFromOcur(sdt.upper(),"D",0)
    sTemp = str_SpacesOut(sTemp)
    if sTemp != "":
       if str_instrBool(sTemp, ":")==False:
          nday = sTemp
       
    # GET HOURS   
    shor = "0"   
    sTemp = str_getSubStringFromOcur(sdt,":",0)
    sTemp = str_right(sTemp,2)
    sTemp = str_SpacesOut(sTemp)
    if sTemp != "":
       nhor = sTemp

    # GET MINUTES
    nmin = "0"
    sTemp = str_getSubStringFromOcur(sdt,":",1)
    sTemp = str_left(sTemp,2)
    sTemp = str_SpacesOut(sTemp)
    if sTemp != "":
       nmin = sTemp

    # GET SECONDS
    nsec = "0"
    sTemp = str_getSubStringFromOcur(sdt,":",2)
    sTemp = str_left(sTemp,2)
    sTemp = str_SpacesOut(sTemp)
    if sTemp != "":
       nsec = sTemp

    # GET MILISECONDS
    nmsec = "0"
    sTemp = str_getSubStringFromOcur(sdt,".",1)
    sTemp = str_SpacesOut(sTemp)
    if sTemp != "":
       nmsec = sTemp
    
    sdtStart = dtStart.strftime(sdtFormat)
    sdtEnd = dtEnd.strftime(sdtFormat)
    
    sRet = ""
    if bReturnCompleteMsg:
       sRet = "Difference between - Start: " + str(sdtStart) + " - End: " + str(sdtEnd) + "\n"
       print(sRet)
       #sRet = sRet + "Elapsed: " + str(sday) + " days, " + str(shor) + " hours, " + str(smin) + " minutes, " + str(sec) + " seconds."
       sRet = sRet + "Elapsed: "
       
    sRet = sRet + str(nday) + " days, " + str(nhor) + " hours, " + str(nmin) + " minutes, " + str(nsec) + " seconds"
    if nmsec != "0":
       sRet = sRet + ", " + str_AddThousandToNumber(str(nmsec), "") + " miliseconds"
    sRet = sRet + "."
    
    #dt_difference(sdtFormat, "2022/08/17-22:28:52", "2022/08/18-06:35:06", False)

    #print(sRet)
    
    return sRet
    
# dt_getCurrentTimeZone ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_getCurrentTimeZone():

    # get local timezone    
    local_tz = str(get_localzone())

    # using now() to get current time
    #current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    current_time = datetime.now(pytz.timezone(local_tz))
    
    # printing current time in india
    #print("The current time is :", str(current_time))

    tz = str(current_time)
    tz = str_right(tz, 6)
    tz = str_left(tz, 3)

    #print("The current time zone is :", str(tz))

    return tz
    
    