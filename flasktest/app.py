from flask import Flask, render_template
import requests
import threading
import time
#from flask_sqlalchemy import SQLAlchemy

#url for openweathermap API request for Dublin
url='http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&units=metric&APPID=7c4d32959a99216eeb3c99efc8000278'

def updateWeatherInfo(url):
   """
   Takes API URL as input, updates weather info every 5 min, stores in global var
   """
   while True:
        weatherDataString=requests.get(url=url)
        global wds
        wds = weatherDataString.json()
        time.sleep(300)
    #weatherDescription = wds['weather'][0]['description']
    #weatherIcon = wds['weather'][0]['icon']
    #temp = str(round(wds['main']['temp']))


APIthread = threading.Thread(name='updateWeatherInfo', target=updateWeatherInfo,args=[url])

#start updateWeatherInfo as background process
APIthread.start()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('weather.html', wds=wds)


if __name__ == "__main__":
    app.run()
