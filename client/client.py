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

DEMO_APP_HOST = os.getenv('DEMO_APP_HOST', 'localhost')
DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'requests.json')
DEMO_APP_URL = "http://" + DEMO_APP_HOST + ":" + DEMO_APP_PORT + "/callhttp"


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

        for request in data['requests']:
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

async_client()