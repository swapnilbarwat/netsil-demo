import os, os.path
# from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import urllib
import tornado.ioloop
import tornado.web

DEMO_APP_HOST = os.getenv('DEMO_APP_HOST', 'localhost')
DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'requests.json')
DEMO_APP_URL = "http://" + DEMO_APP_HOST + ":" + DEMO_APP_PORT + "/callhttp"


def async_client():
    try:
        http_client = AsyncHTTPClient()
    except Exception:
        #print(traceback.format_exc())
        print ( "Unable to create Client")

    with open(DEMO_CONFIG_FILE) as f:
        data=json.loads(f.read())
        f.close()

        for request in data['requests']:
            success_count=int(request['success']['count'])
            req = Request(200)
            reqObJson = json.dumps(req.__dict__)
            # jsonData=urllib.urlencode(reqObJson)
            headers = {'Content-Type': 'application/json'}
            for i in range(success_count):
                try:
                    response = http_client.fetch(
                                                HTTPRequest(DEMO_APP_URL,"POST",headers,body=reqObJson),
                                                callback=self.async_callback(self.on_response),
                                                )
                except Exception as e:
                    print (str(e))
                    pass
                print ( "Ended" + str(success_count))
        # http_client.close()

def handleResponse(response):
    print ("Callback function to handle response")

class Request():
    def __init__(self,response_code):
        self.response_code=response_code

async_client()

# lcount =0
# while lcount < 10000:
#         lcount = lcount +1
#         synchronous_fetch(url = DEMO_APP_URL + "serviceA", lcount=lcount)
#         synchronous_fetch(url = DEMO_APP_URL + "serviceB", lcount=lcount)
