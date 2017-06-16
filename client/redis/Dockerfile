# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install MySQL-python
RUN mkdir -p /usr/local/client && cd /usr/local/client
ENV TERM=xterm\
    MYSQL_HOST='localhost'\
    MYSQL_USER='root'
COPY client.py  /usr/local/client
COPY mysql_requests.json /usr/local/client
WORKDIR /usr/local/client/

ENTRYPOINT python client.py
