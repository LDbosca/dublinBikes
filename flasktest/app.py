from flask import Flask, render_template
#import DBjson
import pymysql
import json
#from flask_sqlalchemy import SQLAlchemy

#login details for AWS RDS DB
host="dbproject.cqkm9hf5jptc.eu-west-1.rds.amazonaws.com"
port=3306
dbname="dublinbikesDB"
user="user"
password="dublinbikes"

bikesQuery = "SELECT * FROM dublinBikesInfo WHERE dateTime=(SELECT MAX(dateTIME) FROM dublinBikesInfo);"
weatherQuery = "SELECT * FROM weatherInfo WHERE dateTime=(SELECT MAX(dateTime) FROM weatherInfo);"

def fetchFromDB(host,port,dbname,user,password,query,jsonString=False):
    '''
    Returns list containing dict for each DB row. If jsonString set to true it returns a json formatted string
    '''
    #import pymysql
    #import json


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
        
    #It is necessary to convert our datetime entry to string to convert to json - in the interests of modularity I
    #have put this in a try/except block, should this code be reused it may not apply
    if jsonString == True:
        try:
            for i in range(len(result)):
                result[i]['dateTime'] = result[i]['dateTime'].strftime('%Y-%m-%d %H:%M')
        except:
            pass
        result = json.dumps(result)
   
    
    
    return result



app = Flask(__name__)


@app.route('/')
def index():
    wds = fetchFromDB(host,port,dbname,user,password,weatherQuery)
    bds = fetchFromDB(host,port,dbname,user,password,bikesQuery)
    return render_template('weatherDateTime.html', wds=wds, bds=bds)


if __name__ == "__main__":
    app.run()
