from flask import Flask, render_template, jsonify
import DBjson
import predictionGenerator
import threading
import datetime
from flask_cors import CORS


#login details for AWS RDS DB
host="dbproject.cqkm9hf5jptc.eu-west-1.rds.amazonaws.com"
port=3306
dbname="dublinbikesDB"
user="user"
password="dublinbikes"

#queries to fetch latest bike/weather info
bikesQuery = "SELECT * FROM dublinBikesInfo WHERE dateTime=(SELECT MAX(dateTIME) FROM dublinBikesInfo);"
weatherQuery = "SELECT * FROM weatherInfo WHERE dateTime=(SELECT MAX(dateTime) FROM weatherInfo);"

forecastURL='http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&units=metric&APPID=7c4d32959a99216eeb3c99efc8000278'

#start updateWeatherInfo as background process - forecast data is stored in global variable called fds
APIthread = threading.Thread(name='updateWeatherForecast', target=DBjson.updateWeatherForecast,args=[forecastURL,1200])
APIthread.start()



app = Flask(__name__)
#CORS prevents Cross-Origin errors due to the fact that json is local
CORS(app)

@app.route('/')
def index():
    wds = DBjson.fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)

    
    return render_template('index.html', wds=wds, bds=bds)

@app.route('/stations')
def stations():
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    return jsonify(bds)

@app.route('/<bikeStation>/<int:unixTime>/<dropOffStation>/<int:dropOffTime>')
def forecast(unixTime,bikeStation,dropOffStation,dropOffTime):
     #json containing forecast for the date/time entered
    futureWeatherJson = DBjson.matchWeatherForecast(unixTime)
    
    #predicted bike availability for getting a bike - availableBikesPickup[0] is the number of bikes available
    availableBikesPickup = predictionGenerator.generatePrediction(bikeStation,unixTime)
    
    #predicted stand availability for dropping off bike - availableBikesDropOff[1] is the number of stations available
    availableBikesDropOff = predictionGenerator.generatePrediction(dropOffStation,dropOffTime)
    
    
    stringTime = datetime.datetime.utcfromtimestamp(unixTime) #convert unixTime into datetime object
    stringTime = stringTime.strftime("%m/%d/%Y, %H:%M:%S") #convert datetime object into string for webpage

    # we also predict the avail bikes and stands +/- 1 hour of the selected time to display the data in a graph
    # unix timestamp is in second so to add/reduce time we simply use the number of seconds
    pickUpTimeMin30m = unixTime - 1800
    pickUpTimeMin1h = unixTime - 3600
    pickUpTimePlus30m = unixTime + 1800
    pickUpTimePlus1h = unixTime + 3600

    dropOffTimeMin30m = dropOffTime - 1800
    dropOffTimeMin1h = dropOffTime - 3600
    dropOffTimePlus30m = dropOffTime + 1800
    dropOffTimePlus1h = dropOffTime + 3600

    #predict for the additionl times
    availableBikesPickupMin30m = predictionGenerator.generatePrediction(bikeStation,pickUpTimeMin30m)
    availableBikesPickupMin1h = predictionGenerator.generatePrediction(bikeStation,pickUpTimeMin1h)
    availableBikesPickupPlus30m = predictionGenerator.generatePrediction(bikeStation,pickUpTimePlus30m)
    availableBikesPickupPlus1h = predictionGenerator.generatePrediction(bikeStation,pickUpTimePlus1h)

    availableBikesDropOffMin30m = predictionGenerator.generatePrediction(dropOffStation,dropOffTimeMin30m)
    availableBikesDropOffMin1h = predictionGenerator.generatePrediction(dropOffStation,dropOffTimeMin1h)
    availableBikesDropOffPlus30m = predictionGenerator.generatePrediction(dropOffStation,dropOffTimePlus30m)
    availableBikesDropOffPlus1h = predictionGenerator.generatePrediction(dropOffStation,dropOffTimePlus1h)

    availBikes = [availableBikesPickupMin30m, availableBikesPickupMin1h, availableBikesPickup, availableBikesPickupPlus30m, availableBikesPickupPlus1h]
    availStnds = [availableBikesDropOffMin30m, availableBikesDropOffMin1h,availableBikesDropOff, availableBikesDropOffPlus30m, availableBikesDropOffPlus1h]



    return jsonify(availBikes, availStnds, futureWeatherJson)

if __name__ == "__main__":
    app.run(debug=True)
