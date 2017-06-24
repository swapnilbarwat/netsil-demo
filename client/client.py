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
import sys

import MySQLdb

import redis

# your gen-py dir
sys.path.append('gen-py')

# Example files
from Example import *
from Example.ttypes import *

# Thrift files 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


DEMO_APP_HOST = os.getenv('DEMO_APP_HOST', '35.184.3.133')
DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'requests.json')
DEMO_APP_URL = "http://" + DEMO_APP_HOST + ":" + DEMO_APP_PORT + "/callhttp"
MYSQL_HOST = os.getenv('MYSQL_HOST', '104.198.234.47')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PWD = os.getenv('MYSQL_PWD', '')
REDIS_HOST = os.getenv('REDIS_HOST', '130.211.238.221')
THRIFT_SERVER = os.getenv("THRIFT_SERVER", "127.0.0.1")

isInsertdone=False

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

    db.ping(True)
    cur = db.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS testdb")
    cur.execute("use testdb")
    cur.execute("DROP TABLE IF EXISTS employee")
    cur.execute("CREATE TABLE employee (id INT(6) NOT NULL AUTO_INCREMENT, fname VARCHAR(30), lname VARCHAR(30), PRIMARY KEY (id))")

    with open(DEMO_CONFIG_FILE) as f:
        data=json.loads(f.read())
        f.close()

        for command in data['mysql']:
            query=command['command']
            count=command['count']
            for i in range(int(count)):
                #if query is insert and already not run
                if((query.find("insert"))):
                    cur.execute("Select count(*) from employee")
                    result=cur.fetchone()
                    #no of records does not match with count in json then keep on inserting.
                    if(result == int(count)):
                        isInsertdone=True
                    else:
                        cur.execute(query)
                        for row in cur:
                            print(row)
                else:
                    cur.execute(query)
                    for row in cur:
                        print(row)
    db.close()

def redisClient():
    r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

    count=10
    for i in range(count):
        print("Adding key redis-key-" + str(i))
        r.set('redis-key-' + str(i), 'redis-value-' + str(i))
        time.sleep(5)
        print("Reading redis-key-" + str(i) + " with value " + str(r.get('redis-key-' + str(i))))
        print ("waiting for 5 sec..")
        #deleting key once insert and read is finished
        r.delete('redis-key-'+str(i))

def thriftClient():
    host = THRIFT_SERVER
    port = 9090

    try:

        # Init thrift connection and protocol handlers
        transport = TSocket.TSocket( host , port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Set client to our Example
        client = Example.Client(protocol)

        # Connect to server
        transport.open()

        # Run showCurrentTimestamp() method on server
        currentTime = client.showCurrentTimestamp()
        print currentTime

        # Assume that you have a job which takes some time
        # but client sholdn't have to wait for job to finish 
        # ie. Creating 10 thumbnails and putting these files to sepeate folders
        client.asynchronousJob()


        # Close connection
        transport.close()

    except Thrift.TException, tx:
        print 'Something went wrong : %s' % (tx.message)

while(1):
    print("Calling http client")
    async_client()
    print("Calling mysql client")
    connectMysqlDB()
    print("calling redis client")
    redisClient()
    print("Calling thrift cleint")
    thriftClient()
    print("Waiting for 5 sec...")
    time.sleep(5)