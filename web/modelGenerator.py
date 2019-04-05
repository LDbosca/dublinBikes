#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:19:12 2019

@author: luke
"""

# Library Imports.
import pandas as pd
import numpy as np
import DBjson
import pickle
import re

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

#create a dataFrame from SQL queried info
host="dbproject.cqkm9hf5jptc.eu-west-1.rds.amazonaws.com"
port=3306
dbname="dublinbikesDB"
user="user"
password="dublinbikes"



def generateModel(host,port,dbname,user,password,station,weekday=True):
    '''
    Generates a predictive model for a given station, saves as a csv file with the name of the station
    '''
    
    #query for one station, contains weather and station info
    oneStationAndWeather = 'SELECT * FROM dublinbikesDB.dublinBikesInfo, dublinbikesDB.weatherInfo WHERE dublinBikesInfo.dateTime = weatherInfo.dateTime AND dublinBikesInfo.stationName="' + station + '";'
    
    #db call
    info = DBjson.fetchFromDB(host,port,dbname,user,password,oneStationAndWeather)
    
    #put info into pandas dataframe
    df = pd.DataFrame(info)
    
    #create columns for day (0-6), hour, minute
    df['weekday'] = df['dateTime'].dt.dayofweek
    df['hour'] = df['dateTime'].dt.hour
    df['minutes'] = df['dateTime'].dt.minute
    
    #create column time - this expresses the time in half hour intervals - 7 is 7am, 7.5 is 7.30am etc.
    df['time'] = np.where(df['minutes'] >= 30, df.hour + 0.5, df.hour)
    
    #create a feature 'rain' - 0 or 1
    df['rain'] = np.where((df['weatherID'] >= 500) & (df['weatherID'] <= 531), 1,0)
    
    #binary encode days so their value has meaning in a polynomial
    df['Monday'] = np.where((df['weekday'] == 0),1,0)
    df['Tuesday'] = np.where((df['weekday'] == 1),1,0)
    df['Wednesday'] = np.where((df['weekday'] == 2),1,0)
    df['Thursday'] = np.where((df['weekday'] == 3),1,0)
    df['Friday'] = np.where((df['weekday'] == 4),1,0)
    df['Saturday'] = np.where((df['weekday'] == 5),1,0)
    df['Sunday'] = np.where((df['weekday'] == 6),1,0)
    
    #drop closed hours to increase accuracy of model
    df = df.drop(df[(df.time > 1) & (df.time < 5)].index)
    
    if weekday==True:
        #drop Sat/Sunday
        df = df.drop(df[df.weekday > 4 ].index)
    else:
        #drop Mon-Fri
        df = df.drop(df[df.weekday < 5].index)
        
    #drop unused columns
    df = df[['dateTime','time','stationBikesAvailable','rain','Monday',
       'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']]

    
    #features to be considered
    if weekday==True:
        features = ['time','rain','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    else:
        features = ['time','rain','Saturday','Sunday']
    
    #input values
    x = df[features]
    #target feature
    y = df.stationBikesAvailable

    #use polynomial of degree 2
    polynomial_features = PolynomialFeatures(degree=2)
    
    #fit input value into polynomial
    x_poly = polynomial_features.fit_transform(x)
    
    model = LinearRegression()
    #train model 
    model.fit(x_poly, y)
    
    #make filename from station name minus whitespace and pkl extension
    if weekday==True:
        filename = re.sub("['/()]", '', station)
        filename = filename.replace(" ","")
        filename = "weekdayModels/" + filename + ".pkl"
    else:
        filename = re.sub("['/()]", '', station)
        filename = filename.replace(" ","")
        filename = "weekendModels/" + filename + ".pkl"
    
    with open(filename,'wb') as handle:
        pickle.dump(model,handle,pickle.HIGHEST_PROTOCOL)





def generateAllModels(host,port,dbname,user,password):
    '''
    Takes a list of stations, generates weekend and weekday models for each, saves in /weekdayModels and
    /weekendModels
    '''
    #query to extract names of stations
    extractStationNames = "SELECT DISTINCT stationName FROM dublinbikesDB.dublinBikesStaticInfo;"
        #DB call to extract station names - stored as list of dicts
    stationNamesListDicts = DBjson.fetchFromDB(host,port,dbname,user,password,extractStationNames)
    stationList=[] 

    #   store station names in a list for easier iteration
    for item in stationNamesListDicts:
        stationList.append(item['stationName'])
    
    
    #generate weekday models
    for station in stationList:
        generateModel(host,port,dbname,user,password,station)
    #generate weekend models    
    for station in stationList:
        generateModel(host,port,dbname,user,password,station,weekday=False)