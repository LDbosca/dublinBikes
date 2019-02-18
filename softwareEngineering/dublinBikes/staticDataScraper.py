#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:43:11 2019

@author: luke ft. Ivan
"""
#not all of these are necessary - mostly requests, datetime and pymysql I think - I loaded up others before I had 
#figured out how to do what I wanted to

import requests
from datetime import datetime
import pymysql
import traceback
import time

currentTime = datetime.now().strftime('%Y-%m-%d %H:%M')

#retrieve dbikes data and store as a string
dburl='https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=a3d2f945558b9f5f4eb7c43a28e4a87a99531d25'
dbds=requests.get(dburl).json()
print(len(dbds))

def getBikesData(i):
    #store each piece of data from the weather info json as a variable so that we may later store it in out MySQL DB
    #most data will be whole numbers - we have rounded up any decimals to simplify data storage in the DB
    
    bikeDataSQL = ""

    stationName = str(dbds[i]['name'])
    bikeDataSQL+= '"' + stationName + '",'

    stationLat = str(dbds[i]['position']['lat'])
    bikeDataSQL+= "'" + stationLat + "',"

    stationLong = str(dbds[i]['position']['lng'])
    bikeDataSQL+= "'" + stationLong + "',"

    stationBanking = str(dbds[i]['banking'])
    bikeDataSQL+= "'" + stationBanking + "',"

    stationStands = str(dbds[i]['bike_stands'])
    bikeDataSQL+= "'" + stationStands + "')"

    insertStatement = "INSERT INTO dublinBikesStaticInfo ( stationName, stationLat, stationLong, stationBanking, stationStands ) VALUES ("
    insertStatement += bikeDataSQL
    print(insertStatement)
    return insertStatement

def writeData(query):
    #login details for AWS RDS DB
    host="dbproject.cqkm9hf5jptc.eu-west-1.rds.amazonaws.com"
    port=3306
    dbname="dublinbikesDB"
    user="user"
    password="dublinbikes"
    
    #create a connection with the details above passed in
    conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)
    #this creates a cursor object that you need to execute operations on the DB
    cursorObject = conn.cursor()
    #executes the insert statement defined above - note you also have to commit it for it to take effect
    cursorObject.execute(query)
    #this is necessary to make the changes executed above take place
    conn.commit()
    #closes the connection to the DB
    conn.close()
    
try:
    for i in range(0,len(dbds)):
        bikesSQL = getBikesData(i)
        writeData(bikesSQL)
        print(i)
except:
    errorLog = open("errors.log","a+")
    errorLog.write("Failed to write to DB at " + currentTime + "\n")
    errorLog.close()

    errorDetails = open("errorDetails.log","a+")
    errorDetails.write("Details of error at " + currentTime + ":\n \n")
    errorDetails.write(traceback.format_exc() + "\n")
    errorDetails.close()  
    
    
    
    