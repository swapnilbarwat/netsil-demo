import json
import os, os.path
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from pprint import pprint


# ENVIORNMENT VARAIBLES initialization

DEMO_APP_PORT = os.getenv('DEMO_APP_PORT', '9000')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")

iniitalized = False

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		print ("NetSil Demo app http server")
        # Need default case if someone did not called valid API #TODO
		self.write("NetSil Demo app http server")

class Request():
    def __init__(self, errors, success):
        self.name = name
        self.clienttouse = clienttouse
        self.errors = errors
        self.success = success

@gen.coroutine
def makeResponse(data, request):
    rCode=int(data.response_code)
    request.set_status(rCode)

    if (rCode == 200):
        print("Sending 200")
        request.write("Sucessful response: 200")
        request.finish()
    elif (rCode == 304):
        print("Sending 304")
        request.finish()
    else:
        print("error with code  " + str(rCode))
        request.write(str(rCode))
        request.finish()

class HttpHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print ("POST ==> calling HttpHandler")
        requestData=Data(self.request.body)
        makeResponse(requestData, self)

class Data(object):
    def __init__(self,data):
        self.__dict__ = json.loads(data)

class Application(tornado.web.Application):
    def __init__(self):
        
        # Handlers defining the url routing.
        handlers = [
                    (r"/testservice", MainHandler),
                    (r"/callhttp", HttpHandler),
                    (r"/intermediatecallpostgres", PostgresHandler),
                    # (r"/intermediatecallbusiness", BusinessHandler),
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

class PostgresHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        print ("POST ==> calling HttpHandler")
        requestData=Data(self.request.body)
        rSucessCount=int(requestData.success)
        for i in range(rSucessCount):
            self.request.set_status(200)

        rExceptionCount=int(requestData.failure)
        for i in range(rExceptionCount):
            try:
                conn = psycopg2.connect("user='wrongpostgresuser' host=" + POSTGRES_HOST + " password='mywrongsecretpassword'")
            except Exception as e:
                print "I am unable to connect to the database"
                self.request.set_status(e.errno)
                self.request.finish()

# class MysqlHandler(tornado.web.RequestHandler):

# class BusinessHandler(tornado.web.RequestHandler):


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
    app.listen(int(DEMO_APP_PORT))
    tornado.ioloop.IOLoop.current().start()


def cleanup():
    tornado.ioloop.IOLoop.current().stop()
    print ("\n======================================================")
    print ("                 Http server stopped                    ")
    print ("========================================================")

# allServices = Services()

if __name__ == "__main__":
    try :
        main()
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

