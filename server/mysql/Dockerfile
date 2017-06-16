# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
#avoid mysql password prompt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install mysql-server -y
RUN update-rc.d mysql defaults
RUN pip install MySQL-python
RUN mkdir -p /usr/local/server && cd /usr/local/server
ENV TERM=xterm\
    MYSQL_HOST='localhost'\
    MYSQL_USER='root'
COPY server.py  /usr/local/server
COPY mysql_data.json /usr/local/server
WORKDIR /usr/local/server/
ENTRYPOINT service mysql restart && python server.py && bash