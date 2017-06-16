import MySQLdb
import json
import os, os.path

import time

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PWD = os.getenv('MYSQL_PWD', '')

DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'mysql_requests.json')

def connectMysqlDB():
    db = MySQLdb.connect(host=MYSQL_HOST,    # your host, usually localhost
                         user=MYSQL_USER,         # your username
                         passwd=MYSQL_PWD,  # your password
                         db="testdb")        # name of the data base

    cur = db.cursor()

    with open(DEMO_CONFIG_FILE) as f:
        data=json.loads(f.read())
        f.close()

        command=data['mysql']['command']
        count=data['mysql']['count']
        

        for i in range(int(count)):
            cur.execute(command)
            print(command)
            for row in cur:
                print(row) 

    db.close()

while(1):
    connectMysqlDB()
    time.sleep(5)
    print ("waiting for 5 sec..")
