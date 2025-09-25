#! /usr/bin/env python3

from str import *
import sys

#------------------------------------------------------------------------------------
def dbsqllite_RecordsCountFromDB(conn, sTable):

    cursT = conn.cursor()

    # --------------------------------------------------------------------------------------
    sSelect = "SELECT count(*) FROM " + sTable
    records = cursT.execute(sSelect).fetchall()
    
    sCount = ""    
    for row in records:
        sCount = str(row[0])
         
    return str(sCount)
