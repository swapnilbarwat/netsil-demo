# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install tornado
RUN mkdir -p /usr/local/client && cd /usr/local/client
ENV TERM=xterm\
    DEMO_APP_HOST='localhost'\
    DEMO_APP_PORT='9000'
COPY client.py  /usr/local/client
COPY requests.json /usr/local/client
WORKDIR /usr/local/client/

CMD python client.py
