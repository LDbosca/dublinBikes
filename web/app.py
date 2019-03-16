from flask import Flask, render_template, jsonify
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

@app.route('/<bikeStation>/<int:unixTime>')
def forecast(unixTime,bikeStation):
    wds = DBjson.fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    futureWeatherJson = DBjson.matchWeatherForecast(unixTime) #json containing forecast for the date/time entered
    stringTime = datetime.datetime.utcfromtimestamp(unixTime) #convert unixTime into datetime object
    stringTime = stringTime.strftime("%m/%d/%Y, %H:%M:%S") #convert datetime object into string for webpage
    return render_template('index.html', futureWeatherJson=futureWeatherJson,forecast=True,wds=wds,bds=bds,bikeStation=bikeStation,stringTime=stringTime)

if __name__ == "__main__":
    app.run(debug=True)