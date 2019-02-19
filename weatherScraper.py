#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 17:43:11 2019

@author: luke
"""
#not all of these are necessary - mostly requests, datetime and pymysql I think - I loaded up others before I had 
#figured out how to do what I wanted to

import requests
from datetime import datetime
import pymysql
import traceback

currentTime = datetime.now().strftime('%Y-%m-%d %H:%M')


def getWeatherData():
    #retrieve weather data and store as a string
    url='http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&units=metric&APPID=7c4d32959a99216eeb3c99efc8000278'
    weatherDataString=requests.get(url=url)
    wds = weatherDataString.json()
    
    #this variable tells us which version of an SQL query to use later
    isWindGust = False
    
    #store each piece of data from the weather info json as a variable so that we may later store it in out MySQL DB
    #most data will be whole numbers - we have rounded up any decimals to simplify data storage in the DB
    weatherDataSQL = ""
    weatherDataSQL += "'" + currentTime + "',"

    weatherID = str(wds['weather'][0]['id'])
    weatherDataSQL += "'" + weatherID + "',"

    weatherMain = wds['weather'][0]['main']
    weatherDataSQL += "'" + weatherMain + "',"

    weatherDescr = wds['weather'][0]['description']
    weatherDataSQL += "'" + weatherDescr + "',"

    weatherIcon = wds['weather'][0]['icon']
    weatherDataSQL += "'" + weatherIcon + "',"

    temp = round(wds['main']['temp'])
    weatherDataSQL += "'" + str(temp) + "',"

    pressure = wds['main']['pressure']
    weatherDataSQL += "'" + str(pressure) + "',"

    humidity = round(wds['main']['humidity'])
    weatherDataSQL += "'" + str(humidity) + "',"

    tempMin = round(wds['main']['temp_min'])
    weatherDataSQL += "'" + str(tempMin) + "',"

    tempMax = round(wds['main']['temp_max'])
    weatherDataSQL += "'" + str(tempMax) + "',"

    visibility = round(wds['visibility'])
    weatherDataSQL += "'" + str(visibility) + "',"

    windSpeed = round(wds['wind']['speed'])
    weatherDataSQL += "'" + str(windSpeed) + "',"

    windDegree = round(wds['wind']['deg'])
    weatherDataSQL += "'" + str(windDegree) + "',"

#wind gust is not always present so we place it in a try/except block
    try:
        windGust = round(wds['wind']['gust'])
        weatherDataSQL += "'" + str(windGust) + "',"
        isWindGust = True
    except:
        pass
    
    clouds = wds['clouds']['all']
    weatherDataSQL += "'" + str(clouds) + "')"

#pick appropriate statement depending on whether there is windGust or not
    if isWindGust:
        insertStatement = "INSERT INTO weatherInfo (dateTime, weatherID, weatherMain, weatherDescr, weatherIcon, temperature, pressure, humidity, tempMin, tempMax, visibility, windSpeed, windDeg, windGust, clouds) VALUES ("
    else:
        insertStatement = "INSERT INTO weatherInfo (dateTime, weatherID, weatherMain, weatherDescr, weatherIcon, temperature, pressure, humidity, tempMin, tempMax, visibility, windSpeed, windDeg, clouds) VALUES ("

    insertStatement += weatherDataSQL
    
    return insertStatement


def writeWeatherData(query):
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
    SQL = getWeatherData()
    writeWeatherData(SQL)
except:
    errorLog = open("errors.log","a+")
    errorLog.write("Failed to write to DB at " + currentTime + "\n")
    errorLog.close()
    
    errorDetails = open("errorDetails.log","a+")
    errorDetails.write("Details of error at " + currentTime + ":\n \n")
    errorDetails.write(traceback.format_exc() + "\n")
    errorDetails.close()  
    
    