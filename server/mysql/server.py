import MySQLdb
import json
import os, os.path

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PWD = os.getenv('MYSQL_PWD', '')

DEMO_CONFIG_FILE = os.getenv('DEMO_CONFIG_FILE', 'mysql_data.json')

db = MySQLdb.connect(host=MYSQL_HOST,    # your host, usually localhost
                     user=MYSQL_USER,         # your username
                     passwd=MYSQL_PWD)
cur = db.cursor()

with open(DEMO_CONFIG_FILE) as f:
    data=json.loads(f.read())
    f.close()

    count=data['employees']['records']
    fname=data['employees']['fname']
    lname=data['employees']['lname']
    print("inserting " + str(count))

    cur.execute("CREATE DATABASE IF NOT EXISTS testdb")
    cur.execute("use testdb")
    cur.execute("DROP TABLE IF EXISTS employee")
    cur.execute("CREATE TABLE employee (id INT(6) NOT NULL AUTO_INCREMENT, fname VARCHAR(30), lname VARCHAR(30), PRIMARY KEY (id))")
    for counter in range(int(count)):
        cur.execute("INSERT INTO employee (fname, lname) VALUES (%s, %s)", (fname,lname))
        print(cur._executed)

db.commit()
db.close()