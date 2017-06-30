import json
import os, os.path
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from pprint import pprint

from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPClient

from tornado.httpclient import AsyncHTTPClient

import psycopg2

# ENVIORNMENT VARAIBLES initialization
DEMO_APP_INTERMEDIATE_PORT = os.getenv('DEMO_APP_INTERMEDIATE_PORT', '9010')
DEMO_APP_HOST = os.getenv('DEMO_APP_URL','127.0.0.1')
DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
DEMP_APP_URL = "http://" + DEMO_APP_HOST + ":" + DEMO_APP_PORT

iniitalized = False

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print ("NetSil intermediate demo app http server")
        # Need default case if someone did not called valid API #TODO
		self.write("NetSil intermediate demo app http server")

class Request():
    def __init__(self, errors, success):
        self.name = name
        self.clienttouse = clienttouse
        self.errors = errors
        self.success = success

class PostgresHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print ("POST ==> calling PostgresHandler")
        requestData=Data(self.request.body)
        succesCount=requestData.success
        failCount=requestData.failure
        print(succesCount)
        print(failCount)
        for i in range(int(failCount)): 
            headers = {'Content-Type': 'application/json'}
            try:
                http_client = HTTPClient()
                API_URL = DEMP_APP_URL + "/intermediatecallpostgresfail"
            except Exception as e:
                print ( "Unable to create Client" + str(e))
            try:
                http_request = HTTPRequest(API_URL,"POST",headers,body=self.request.body)
                http_client.fetch(http_request)
            except HTTPError as e:
                print(HTTPError)
                pass
            else:
                response = http_client.fetch(http_request)
                responseJSON=json.dumps(response.__dict__)
                self.write(responseJSON)

        for i in range(int(succesCount)): 
            headers = {'Content-Type': 'application/json'}
            try:
                http_client = HTTPClient()
                API_URL = DEMP_APP_URL + "/intermediatecallpostgressuccess"
            except Exception as e:
                print ( "Unable to create Client" + str(e))
            try:
                http_request = HTTPRequest(API_URL,"POST",headers,body=self.request.body)
                http_client.fetch(http_request)
            except HTTPError as e:
                print(HTTPError)
                pass
            else:
                response = http_client.fetch(http_request)
                responseJSON=json.dumps(response.__dict__)
                self.write(responseJSON)

        http_client.close()

class MysqlHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print ("POST ==> calling MysqlHandler")
        requestData=Data(self.request.body)
        makeResponse(requestData, self)

class BusinessHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print ("POST ==> calling BusinessHandler")
        requestData=Data(self.request.body)
        makeResponse(requestData, self)


class Data(object):
    def __init__(self,data):
        self.__dict__ = json.loads(data)

class Application(tornado.web.Application):
    def __init__(self):
        
        # Handlers defining the url routing.
        handlers = [
                    (r"/callpostgres", PostgresHandler),
                    (r"/callbusiness", BusinessHandler),
                    (r".*",   MainHandler),
                    ]
            
        # Settings:
        settings = dict(            cookie_secret = "43osdETzKXasdQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                                    template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                    static_path=os.path.join(os.path.dirname(__file__), "static"),
                        # should be false to use POST method
                                    xsrf_cookies= False,
                                    autoescape="xhtml_escape",
                                    # apptitle used as page title in the template.
                                    apptitle = 'Demo App For MicroServices',
                        )
                    
                    # Call super constructor.
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    global iniitalized
    tornado.options.parse_command_line()
    app = Application ()
    # TODO ADD NETSIL BANNER
    print ("======================================================")
    print ("                Http server started                   ")
    print ("======================================================")
    # configure()
    # allServices.printServices()
    iniitalized = True
    app.listen(int(DEMO_APP_INTERMEDIATE_PORT))
    tornado.ioloop.IOLoop.current().start()


def cleanup():
    tornado.ioloop.IOLoop.current().stop()
    print ("\n======================================================")
    print ("                 Http server stopped                    ")
    print ("========================================================")
    

# def BusinessHttpClient():


# allServices = Services()

if __name__ == "__main__":
    try :
        main()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

