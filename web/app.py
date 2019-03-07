from flask import Flask, render_template, jsonify
import DBjson

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

app = Flask(__name__)
#CORS prevents Cross-Origin errors due to the fact that json is local
CORS(app)


@app.route('/')
def index():
    wds = DBjson.fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = DBjson.fetchFromDB(host,port,dbname,user,password,bikesQuery)
    return render_template('weatherDateTime.html', wds=wds, bds=bds)

@app.route('/stations')
def stations():
    bds = fetchFromDB(host,port,dbname,user,password,bikesQuery)
    return jsonify(bds)



if __name__ == "__main__":
    app.run(debug=True)
