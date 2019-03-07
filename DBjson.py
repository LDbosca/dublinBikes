#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 11:56:35 2019

@author: luke
"""

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
        cursorObject.execute(query)
    #this is necessary to make the changes executed above take place
        result = cursorObject.fetchone()
        #closes the connection to the DB
        conn.close()
        
    #It is necessary to convert our datetime entry to string to convert to json - in the interests of modularity I
    #have put this in a try/except block, should this code be reused it may not apply
    try:
        result['dateTime'] = result['dateTime'].strftime('%Y-%m-%d %H:%M')
        jsonResult = json.dumps(result)
    except:
        pass
        
    return jsonResult
