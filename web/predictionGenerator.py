#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:38:55 2019

@author: luke
"""

import DBjson
import re
import pickle
import pandas as pd
from datetime import datetime
from numStands import numStands #number of stands per station saved in a file to limit DB calls

from sklearn.preprocessing import PolynomialFeatures




def generatePrediction(stationName,unixTime):
    """
    Takes bike station and unix time, returns predicted number of bikes/stands at given time (tuple)  
    
    """
        
    #create datetime object from unix time
    predictionDate = datetime.fromtimestamp(unixTime)
    #fetch weather data for requested time
    futureWeatherJson = DBjson.matchWeatherForecast(1554368925)
    
    
    #conditionally create values to put in dataframe for prediction
    if 500 <= futureWeatherJson['weather'][0]['id'] <= 531:
        rain = 1
    else:
        rain = 0
    
    #divide time into 30 minute intervals for dataframe
    if predictionDate.minute < 30:
        time = predictionDate.hour
    else:
        time = predictionDate.hour + 0.5
    
    #array of days to put in dataframe
    days = [0,0,0,0,0,0,0]
    #extract day from datetime object
    weekday = predictionDate.weekday()
    #set index of applicable weekday to equal 1
    days[weekday] = 1
    #slice list depending on whether we're calling a weekday or weekend model
    if weekday < 5:
        days = days [0:5]
    else:
        days = days [5:]
    #combine all relevant data into one list to generate dataframe 
    data = [time, rain] + days
        
    #generate a dataframe from unixTime - generate different columns for weekdays and weekends
    if weekday < 5:
        df = pd.DataFrame([data], columns = ['time','rain','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    else:
        df = pd.DataFrame([data], columns = ['time','rain','Saturday', 'Sunday'])
        
    #remove special characters and whitespace from station name to generate file name
    filename = re.sub("['/()]", '', stationName)
    filename = filename.replace(" ","")
    #generate file path to load model
    if weekday < 5:
        filePath = "weekdayModels/" + filename + ".pkl"
    else:
        filePath = "weekendModels/" + filename + ".pkl"
    
    with open(filePath, 'rb') as handle:
        model = pickle.load(handle)
        
    #use polynomial of degree 2
    polynomial_features = PolynomialFeatures(degree=2)
    #fit features into polynomial   
    df_poly = polynomial_features.fit_transform(df)
    #predict using loaded model
    prediction = model.predict(df_poly)
    
    ans = (round(prediction[0]),round((numStands[stationName])-prediction[0]))
    
    #return tuple containing available bikes and available stands
    return ans

