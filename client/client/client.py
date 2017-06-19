import os, os.path
from tornado import gen
import json
import urllib
import tornado.ioloop
import tornado.web
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPClient

from tornado.httpclient import AsyncHTTPClient

import time

import MySQLdb

import redis

DEMO_APP_HOST = os.getenv('DEMO_APP_HOST', 'localhost')
DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'requests.json')
DEMO_APP_URL = "http://" + DEMO_APP_HOST + ":" + DEMO_APP_PORT + "/callhttp"
MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PWD = os.getenv('MYSQL_PWD', '')
REDIS_HOST = os.getenv('REDIS_HOST', '172.17.0.2')


def async_client():
    try:
        http_client = HTTPClient()
        # http_client = tornado.httpclient.AsyncHTTPClient(
    except Exception as e:
        #print(traceback.format_exc())
        print ( "Unable to create Client" + str(e))

    with open(DEMO_CONFIG_FILE) as f:
        data=json.loads(f.read())
        f.close()

        for request in data['http']:
            success_count=int(request['success']['count'])
            sendSuccessRequests(http_client, success_count)
            errorList=request['errors']
            sendErrorRequests(http_client, errorList)
            
        http_client.close()

def handleResponse(response):
    print ("Callback function to handle response")

def sendSuccessRequests(http_client, request_count):
    req = Request(200)
    reqObJson = json.dumps(req.__dict__)
    headers = {'Content-Type': 'application/json'}
    lcount=0
    while lcount < request_count:
        try:
            http_request = HTTPRequest( DEMO_APP_URL,"POST",headers,body=reqObJson  )
            response = http_client.fetch(http_request)
            lcount=lcount+1
        except Exception as e:
            print (str(e))
            pass
        print ( "Request sent count -" + str(lcount))

def sendErrorRequests(http_client, errorList):
    for error in errorList:
        headers = {'Content-Type': 'application/json'}
        lcount=0
        # http_client = AsyncHTTPClient()
        print(error['count'])
        while lcount < int(error['count']):
            req = Request(error['http_code'])
            reqObJson = json.dumps(req.__dict__)
            try:
                # http_request = HTTPRequest( DEMO_APP_URL,"POST",headers,body=reqObJson  )
                # response = http_client.fetch(http_request)
                http_request = HTTPRequest( DEMO_APP_URL,"POST",headers,body=reqObJson  )
                http_client.fetch(http_request)
                # tornado.ioloop.IOLoop.instance().start()
                lcount=lcount+1
            except HTTPError as e:
                lcount = lcount + 1
                pass
            except Exception as e:
                print (str(e))
            print ( "Request with " + str(error['http_code']) + " sent with count -" + str(lcount))

def handle_request(response):
    '''callback needed when a response arrive'''
    if response.error:
        print "Error:", response.error
        pass
    else:
        print 'called'
        print response.body


class Request():
    def __init__(self,response_code):
        self.response_code=response_code

def connectMysqlDB():
    db = MySQLdb.connect(host=MYSQL_HOST,    # your host, usually localhost
                         user=MYSQL_USER,         # your username
                         passwd=MYSQL_PWD)  # your password

    cur = db.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS testdb")
    cur.execute("use testdb")
    cur.execute("DROP TABLE IF EXISTS employee")
    cur.execute("CREATE TABLE employee (id INT(6) NOT NULL AUTO_INCREMENT, fname VARCHAR(30), lname VARCHAR(30), PRIMARY KEY (id))")

    with open(DEMO_CONFIG_FILE) as f:
        data=json.loads(f.read())
        f.close()

        for command in data['mysql']:
            command=data['mysql']['command']
            count=data['mysql']['count']
            for i in range(int(count)):
                #if query is insert and already not run
                if((command.find("insert")) and (not isInsertdone)):
                    cur.execute("Select count(*) from employee")
                    result=cur.fetchone()
                    #no of records does not match with count in json then keep on inserting.
                    if(result == int(count)):
                        isInsertdone=true
                    else:
                        cur.execute(command)
                        for row in cur:
                            print(row)
                else:
                    cur.execute(command)
                    for row in cur:
                        print(row)
    db.close()

def redisClient():
    r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

    i=0
    while(1):
        print("Adding key redis-key-" + str(i))
        r.set('redis-key-' + str(i), 'redis-value-' + str(i))
        time.sleep(5)
        print("Reading redis-key-" + str(i) + " with value " + r.get('key-'+str(i)))
        print ("waiting for 5 sec..")
        #deleting key once insert and read is finished
        r.delete('redis-key-'+str(i))
        i=i+1

isInsertdone = False
while(1):
    print("Calling http client")
    async_client()
    print("Calling mysql client")
    connectMysqlDB()
    print("calling redis client")
    redisClient()
    print("Waiting for 5 sec...")
    time.sleep(5)
