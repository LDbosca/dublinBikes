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
        cursor.execute(query)
    #this is necessary to make the changes executed above take place
        result = cursor.fetchall()
        #closes the connection to the DB
        conn.close()

    return result


def updateWeatherForecast(url,interval):
   """
   Takes API URL and update interval (seconds), fetches weather info at intervals, stores in a global - fds
   """
   while True:
        forecastDatastring=requests.get(url=url)
        global fds #weather info stored in global as this function will run in the background and never return a  value
        fds = forecastDatastring.json()
        time.sleep(interval) #sets the interval between API calls

#NB - matchWeatherForecast should take two parameters - the forecast json and unixTime - I had trouble with flask
#and scope so I've temporarily using the global fds in it directly. I'll fix this at some point because it's
#AWFUL coding! Luke xxx
def matchWeatherForecast(unixTime):
    """
    Returns nearest matching weather forecast data - returns False if date is outside forecast range
    """
    for i in range(len(fds['list'])):
        if unixTime <= fds['list'][i]['dt']:
            return fds['list'][i]['main']['temp']
    return False

