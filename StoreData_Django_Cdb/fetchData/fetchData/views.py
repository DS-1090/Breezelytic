import requests
from django.http import JsonResponse
import csv
api_key= "579af2f50a3f2c8cf6fc4b1479917cc8f62babc3"

headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key
}

loc='hyderabad'

#FOR DB UPDATES

#fetch aqi values for that location from the api 
def fetchLocData(request):
    url = f"https://api.waqi.info/feed/{loc}/?token={api_key}"
    response = requests.get(url, headers=headers)
    if(response.status_code != 200):
        return JsonResponse({"result": "error"})
    data = response.json()
    return cleanData(data)

#extract required vals from json response
def cleanData(data):
    location_value = data["data"]["city"]["name"]
    pm25_value = data["data"]["forecast"]["daily"]["pm25"]
    #print(location_value)
    if(pm25_value == []):
        return JsonResponse({"result": "pm25 values not found"})
    
    #storing in cassandra
    #sendToCassandra(location_value, pm25_value)

    #storing in json
    with open("data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date",  "location", "avg_pm25","max_pm25", "min_pm25"])
        for record in pm25_value:
            date = record["day"]
            avg_pm25 = record["avg"]
            max_pm25 = record["max"]
            min_pm25 = record["min"]
            writer.writerow([date,  location_value, avg_pm25, max_pm25, min_pm25])

    print("CSV file saved successfully!")
    return JsonResponse({"result": "success"})

#send it to cassandra
import json
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

def sendToCassandra(location_value, pm25_value):

    #username and pw is admin
    CASSANDRA_HOST = "cassdb"  

    auth_provider = PlainTextAuthProvider('admin', 'admin')  
    cluster = Cluster([CASSANDRA_HOST], auth_provider=auth_provider, port=9042)
    session = cluster.connect()

 


    print(session.execute("SELECT release_version FROM system.local").one())

    #single node with  0 replicas so its not fault tolerant
    session.execute("CREATE KEYSPACE IF NOT EXISTS aqdata WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")
    session.set_keyspace('aqdata')

    session.execute("CREATE TABLE IF NOT EXISTS pm25 (date TEXT PRIMARY KEY,  location TEXT,   avg_pm25 INT,    max_pm25 INT,    min_pm25 INT);")
    for record in pm25_value:
        session.execute("""
            INSERT INTO pm25 (date, location, avg_pm25, max_pm25, min_pm25)
            VALUES (%s, %s, %s, %s, %s)
        """, (record["day"], location_value, record["avg"], record["max"], record["min"]))
    
    print("Data inserted into the Cassandra DB")
    #cluster.shutdown()



'''
django logs:
[02/Mar/2025 18:38:49] "GET / HTTP/1.1" 404 2468
Data inserted into the Cassandra DB
[02/Mar/2025 18:38:57] "GET /setLocID/ HTTP/1.1" 200 21
'''

#FOR FRONTEND  APP

#current data of the location FETCHED FROM API
#set location using value sent from frontend flutter app
def setLocID(request):
    global loc
    loc = request.GET.get('location', 'hyderabad')

def sendtoApp(request):
    print('connected')
    setLocID(request)
    url = f"https://api.waqi.info/feed/{loc}/?token={api_key}"
    response = requests.get(url)
    if(response.status_code != 200):
        return JsonResponse({"result": "error"})
    data = response.json()
    return JsonResponse(data, safe=False)



#Records fetched from Spark
from django.http import JsonResponse
from .processData import fetchRecords   

def fetchrecords(request):
    data = fetchRecords()   
    return JsonResponse(data, safe=False)



