# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install tornado
RUN pip install psycopg2
RUN mkdir -p /usr/local/k8s_microsim && cd /usr/local/k8s_microsim
COPY server.py /usr/local/k8s_microsim
WORKDIR /usr/local/k8s_microsim/

ENV DEMO_APP_PORT=9000
ENV TERM=xterm

CMD python server.py