# -*- coding: UTF-8 -*-

from datetime import datetime
from datetime import timedelta

# for timezone()
import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

from str import *

sDateTimeF = ".%f"
sDateTimeFZero = "000000"
sDateTimePoint = "."

sDateTimeFormatSuggested = "%Y/%m/%d-%H:%M:%S.%f"

# dt_now ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_now(sFormat):
    if str(sFormat)=="":
       sFormat = sDateTimeFormatSuggested
    
    dateStart = datetime.now()    
    return dateStart.strftime(sFormat)
    
# dt_difference_sec ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference_sec(dtStart, dtEnd):
    dt = dtStart - dtEnd
    return str(dt.total_seconds())

# dt_difference_sec ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference_isFractionInData(sDt):
    sFraction = dt_difference_get_fraction(sDt)
    bReturn = True
    if len(sFraction) != len(sDateTimeFZero):
       bReturn = False
    #print("dt_difference_isFractionInData - sDt = " + sDt + " - return = " + str(bReturn))
    return bReturn

# dt_difference_get_fraction ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference_get_fraction(sDt):
    sDt = str(sDt)
    sFraction = str_mid(sDt, len(sDt)-len(sDateTimeFZero), len(sDateTimeFZero))
    sFraction = str(sFraction)
    #print("dt_difference_get_fraction - sDt = " + sDt + " - sFraction = " + sFraction)
    if "-" in sFraction or "." in sFraction or ":" in sFraction:
       sFraction = ""

    #print("dt_difference_get_fraction - sDt = " + sDt + " - sFraction = " + sFraction)
    return sFraction

# dt_difference_testing ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference_testing():
    
    n = 1
    dtNow1 = datetime.now()   
    sdtFormat = sDateTimeFormatSuggested
    date1 = dtNow1.strftime(sdtFormat)
    dtNow = datetime.now()   
    date2 = dtNow.strftime(sdtFormat)
    sDif = dt_difference(sdtFormat, date1, date2, False)
    print(str(n) + ". dt_difference_testing - date1 = " + str(date1) + " - date2 = " + str(date2) + " - difference: " + str(sDif))
    n = n + 1

    sdtFormat = "%Y-%m-%d %H.%M.%S.%f"
    date1 = dtNow1.strftime(sdtFormat)
    dtNow = datetime.now()   
    date2 = dtNow.strftime(sdtFormat)
    sDif = dt_difference(sdtFormat, date1, date2, False)
    print(str(n) + ". dt_difference_testing - date1 = " + str(date1) + " - date2 = " + str(date2) + " - difference: " + str(sDif))
    n = n + 1

    sdtFormat = "%Y/%m/%d-%H:%M:%S.%f"
    date1 = dtNow1.strftime(sdtFormat)
    dtNow = datetime.now()   
    date2 = dtNow.strftime(sdtFormat)
    sDif = dt_difference(sdtFormat, date1, date2, False)
    print(str(n) + ". dt_difference_testing - date1 = " + str(date1) + " - date2 = " + str(date2) + " - difference: " + str(sDif))
    n = n + 1

    sdtFormat = "%Y/%m/%d-%H:%M:%S"
    date1 = dtNow1.strftime(sdtFormat)
    dtNow = datetime.now()   
    date2 = dtNow.strftime(sdtFormat)
    sDif = dt_difference(sdtFormat, date1, date2, False)
    print(str(n) + ". dt_difference_testing - date1 = " + str(date1) + " - date2 = " + str(date2) + " - difference: " + str(sDif))
    n = n + 1

    sdtFormat = "%Y/%m/%d-%H.%M.%S"
    date1 = dtNow1.strftime(sdtFormat)
    dtNow = datetime.now()   
    date2 = dtNow.strftime(sdtFormat)
    sDif = dt_difference(sdtFormat, date1, date2, False)
    print(str(n) + ". dt_difference_testing - date1 = " + str(date1) + " - date2 = " + str(date2) + " - difference: " + str(sDif))
    n = n + 1

    return

# dt_difference ---------------------------------------------------------------------------------------------------------------------------------------------------------
def dt_difference(sdtFormat, dtStart, dtEnd, bReturnCompleteMsg):
    

    sdtStart = str(dtStart)
    sdtEnd = str(dtEnd)

    #IT IS NEEDED THE FRACTION POR DELTA
    #Example 1: dtProcessGblDateTimeFormat = "%Y-%m-%d %H.%M.%S.%f"
    #Example 2: sdtFormat: %Y/%m/%d-%H:%M:%S.%f

    if not sDateTimeF in sdtFormat:
       sdtFormat = sdtFormat + sDateTimeF

    #CHECKING THE FRACTION
    #strftime: Formats a datetime object into a human-readable string according to a specified format code.
    if not dt_difference_isFractionInData(sdtStart):
       sdtStart = sdtStart + sDateTimePoint + sDateTimeFZero
       dtStart = datetime.strptime(sdtStart, sdtFormat)
    else:
       dtStart = datetime.strptime(str(dtStart),sdtFormat)

    if not dt_difference_isFractionInData(sdtEnd):
       sdtEnd = sdtEnd + sDateTimePoint + sDateTimeFZero
       dtEnd = datetime.strptime(sdtEnd, sdtFormat)
    else:   
       dtEnd = datetime.strptime(str(dtEnd),sdtFormat)

    #print("dt_difference - sdtFormat: " + str(sdtFormat))

    #strptime: Parses a string representation of a date and time and converts it into a datetime object.

    #print("dt_difference - Start: " + str(dtStart))
    #print("dt_difference - End: " + str(dtEnd))
       
    #sFormatDT = "%d/%m/%Y-%H:%M:%S"
    #sFormatDT = "%Y%m%d%H%M%S"
    
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
       sRet = sRet + ", " + str_AddThousandToNumber(str(nmsec), "") + " milliseconds"
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
    
    