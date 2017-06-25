# Netsil creating external client.

- to start client from outside of the cluster, please use following steps:

1) get external ip's of the all service using command: kubectl get services
2) Each service will be assigned an external ip. Copy those in the following command:
 ''' docker run -d -e "DEMO_APP_HOST=104.155.148.71" -e "MYSQL_HOST=35.184.2.254" -e "REDIS_HOST=35.184.6.11" -e "THRIFT_SERVER=130.211.122.154" harshals/netsil_client '''
