# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install tornado asyncmc Tornado-MySQL
RUN pip install git+https://github.com/evilkost/brukva.git
RUN mkdir -p /usr/local/client && cd /usr/local/client
ENV TERM=xterm\
    DEMO_APP_HOST='localhost'\
    DEMO_APP_PORT='9000'
COPY run.py  /usr/local/client
WORKDIR /usr/local/client/

ENV TERM=xterm
CMD python run.py
