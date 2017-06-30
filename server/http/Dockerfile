# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install tornado
RUN pip install psycopg2
RUN mkdir -p /usr/local/k8s_microsim && cd /usr/local/k8s_microsim
RUN apt-get install nginx -y
ADD ssl /etc/nginx/ssl
RUN rm /etc/nginx/sites-enabled/*
COPY ssl/netsil.conf /etc/nginx/sites-enabled/
COPY server.py /usr/local/k8s_microsim
WORKDIR /usr/local/k8s_microsim/

ENV DEMO_APP_PORT=9000
ENV TERM=xterm

CMD service nginx restart && python server.py