# -*- coding: UTF-8 -*-

from datetime import datetime

def valid_date(dt, format):
    
    isValidDate = True
    
    if dt is None:
       return False

    if format is None:
       #format = "%Y-%m-%d"
       format = "%d/%m/%Y"
       
    try:
        datetime.strptime(dt, format)
    except ValueError:
        isValidDate = False    
    return isValidDate


def date_day(dt, bDayFirst):
    if bDayFirst == True:
    	return str(dt[:2])
    else:
      return str(dt[3:5])

    
def date_month(dt, bMonthFirst):
    if bMonthFirst == True:
    	return str(dt[:2])
    else:
       return str(dt[3:5])
       
    
def date_year(dt):
    return str(dt[6:10])


def date_day_first(dt):
    return date_day(dt, True)
    
def date_day_second(dt):
    return date_day(dt, False)
    
def date_month_first(dt):
    return date_month(dt, True)

def date_month_second(dt):
    return date_month(dt, False)
