# The base image
FROM python:2.7
# Install dependencies
RUN apt-get clean && apt-get update
RUN pip install thrift
RUN mkdir -p /usr/local/thrift && cd /usr/local/thrift
COPY PythonServer.py /usr/local/thrift
ADD gen-py /usr/local/thrift/gen-py
WORKDIR /usr/local/thrift/
ENV TERM=xterm

CMD python PythonServer.py