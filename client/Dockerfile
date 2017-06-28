# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN apt-get install netcat -y
RUN pip install tornado
RUN pip install redis
RUN pip install MySQL-python
RUN pip install thrift
RUN pip install statsd
RUN pip install psycopg2
RUN pip install boto3
RUN apt-get install libmemcached-dev
RUN pip install pylibmc
RUN mkdir -p /usr/local/client && cd /usr/local/client
ENV TERM=xterm
ENV DEMO_APP_HOST='localhost'
ENV DEMO_APP_PORT='9000'
ENV MYSQL_HOST='127.0.0.1'
ENV MYSQL_USER='root'
ENV REDIS_HOST='127.0.0.1'
COPY client.py  /usr/local/client
COPY requests.json /usr/local/client
ADD gen-py /usr/local/client/gen-py
COPY ssl/netsil.key /etc/ssl/certs
COPY ssl/netsil.crt /etc/ssl/certs
RUN c_rehash
WORKDIR /usr/local/client/

CMD python client.py