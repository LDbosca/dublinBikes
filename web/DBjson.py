#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 11:56:35 2019

@author: luke
"""

import pymysql
import time
import requests

def fetchFromDB(host,port,dbname,user,password,query):
    '''
    Takes login details and query and returns result as json string - also converts dateTime to string format
    '''
    #create a connection with the details above passed in
    conn = pymysql.connect(host, user=user,port=port, passwd=password, db=dbname)
    #this creates a cursor object that you need to execute operations on the DB - this
    cursorObject = conn.cursor(pymysql.cursors.DictCursor)
    #executes the insert statement defined above - note you also have to commit it for it to take effect

    with cursorObject as cursor:
        cursorObject.execute(query)
    #this is necessary to make the changes executed above take place
        result = cursorObject.fetchall()
        #closes the connection to the DB
        conn.close()

    return result



#url for openweathermap API request for Dublin
#url='http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&units=metric&APPID=7c4d32959a99216eeb3c99efc8000278'

def updateWeatherForecast(url,interval):
   """
   Takes API URL and update interval (seconds), fetches weather info at intervals, stores in a global - fds
   """
   while True:
        foreCastDatastring=requests.get(url=url)
        global fds
        fds = foreCastDatastring.json()
        time.sleep(interval)



