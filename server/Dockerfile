# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install tornado asyncmc Tornado-MySQL
RUN pip install git+https://github.com/evilkost/brukva.git
RUN mkdir -p /usr/local/microsim && cd /usr/local/microsim
ENV TERM=xterm
COPY server.py services.json  /usr/local/microsim/
WORKDIR /usr/local/microsim/

ENV DEMO_APP_PORT=9000\
	DEMO_CONFIG_FILE='services.json'\
	REDIS_HOST=redis_container''\
	REDIS_PORT='6379'\
	MEMCACHED_HOST='memcached_container'\
	MEMCACHED_PORT='11211'\
	MYSQL_HOST='mysql_container'\
	MYSQL_PORT='3306'\
	MYSQL_USER='root'\
	MYSQL_PWD='abc123'\
	MYSQL_DB='mysql'
ENV TERM=xterm
CMD python server.py
