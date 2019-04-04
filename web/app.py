from flask import Flask, render_template, jsonify
from flask_googlecharts import GoogleCharts, BarChart
import DBjson
import threading
import datetime
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy

#login details for AWS RDS DB
host="dbproject.cqkm9hf5jptc.eu-west-1.rds.amazonaws.com"
port=3306
dbname="dublinbikesDB"
user="user"
password="dublinbikes"

bikesQuery = "SELECT * FROM dublinBikesInfo WHERE dateTime=(SELECT MAX(dateTIME) FROM dublinBikesInfo);"
weatherQuery = "SELECT * FROM weatherInfo WHERE dateTime=(SELECT MAX(dateTime) FROM weatherInfo);"

forecastURL='http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&units=metric&APPID=7c4d32959a99216eeb3c99efc8000278'

#start updateWeatherInfo as background process - forecast data is stored in global variable called fds
APIthread = threading.Thread(name='updateWeatherForecast', target=DBjson.updateWeatherForecast,args=[forecastURL,1200])
APIthread.start()



app = Flask(__name__)
#CORS prevents Cross-Origin errors due to the fact that json is local
# CORS(app)
# Setup GoogleCharts instance
charts = GoogleCharts(app)
chartDisplay=False

@app.route('/')
def index():
    wds = DBjson.fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    AvailabilityChart = BarChart("AvailabilityChart", options={"title": "Predicted Bike Availability",
                                                  "width": 700,
                                                  "height": 300, "legend":'none'}) # Need to setup empty chart to avoid error in html.
    charts.register(AvailabilityChart) # Allows the chart to be called from html file.
    
    return render_template('index.html', wds=wds, bds=bds)

@app.route('/stations')
def stations():
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    return jsonify(bds)

@app.route('/<bikeStation>/<int:unixTime>/<dropOffStation>/<int:dropOffTime>')
def forecast(unixTime,bikeStation,dropOffStation,dropOffTime):
    wds = DBjson.fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    #json containing forecast for the date/time entered
    futureWeatherJson = DBjson.matchWeatherForecast(unixTime)

    #predicted bike availability for getting a bike - availableBikesPickup[0] is the number of bikes available
    availableBikesPickup = predictionGenerator.generatePrediction(bikeStation,unixTime)

    #predicted stand availability for dropping off bike - availableBikesDropOff[1] is the number of bikes available
    availableBikesDropOff = predictionGenerator.generatePrediction(dropOffStation,dropOffTime)
    stringTime = datetime.datetime.utcfromtimestamp(unixTime) #convert unixTime into datetime object
    stringJustTime = stringTime.strftime("%H:%M:%S") #convert time object into string for webpage, graphing.
    stringTime = stringTime.strftime("%m/%d/%Y, %H:%M:%S") #convert datetime object into string for webpage

#    Creates graph and populates
    AvailabilityChart = BarChart("AvailabilityChart", options={"title": "Predicted Bike Availability",
                                                  "width": 700,
                                                  "height": 300, "legend":'none'})
    AvailabilityChart.add_column("string", "PredictedTime")
    AvailabilityChart.add_column("number", "Predicted Available Bikes")
    AvailabilityChart.add_rows([[stringJustTime, 20],[stringJustTime, 10], [stringJustTime, 30]]) # These values will be pulled from the ML model.
    charts.register(AvailabilityChart)
    
    return render_template('index.html', futureWeatherJson=futureWeatherJson,forecast=True,wds=wds,bds=bds,bikeStation=bikeStation,stringTime=stringTime)

if __name__ == "__main__":
    app.run(debug=True)