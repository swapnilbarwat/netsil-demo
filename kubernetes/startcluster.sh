#!/usr/bin/env bash

echo "starting netsil demo cluster.."
echo "creating deployments.."
kubectl create -f deployments/http-server.yml
kubectl create -f deployments/intermediate-server.yml
kubectl create -f deployments/memcached.yml
kubectl create -f deployments/mysql.yml
kubectl create -f deployments/postgres.yml
kubectl create -f deployments/redis.yml
kubectl create -f deployments/thrift-server.yml
kubectl create -f deployments/cassandra.yml
kubectl create -f deployments/dynamodb-local.yml

echo "creating services.."
kubectl create -f services/cassandra_service.yml
kubectl create -f services/dynamodb-server.yml
kubectl create -f services/http_server_services.yml
kubectl create -f services/intermediate-service.yml
kubectl create -f services/memcached_service.yml
kubectl create -f services/mysql_service.yml
kubectl create -f services/postgres_service.yml
kubectl create -f services/redis_service.yml
kubectl create -f services/thrift_server.yml

echo "creating config map.."
kubectl create -f configmap.yml

echo "creating client.."
kubectl create -f deployments/client.yml

echo "netsil demo cluster created."