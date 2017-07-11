echo "deleting cluster.."
kubectl delete deploy cassandra
kubectl delete deploy dynamodb
kubectl delete deploy http-server
kubectl delete deploy intermediate-http-server
kubectl delete deploy memcached
kubectl delete deploy mysql-server
kubectl delete deploy netsil-client
kubectl delete deploy postgres
kubectl delete deploy redis
kubectl delete deploy thrift-server

echo "deleting config map.."
kubectl delete configmap http-error-workload

echo "deleting service"
kubectl delete service cassandra-server
kubectl delete service dynamodb
kubectl delete service http-server
kubectl delete service intermediate-http-service
kubectl delete service memcached-server
kubectl delete service mysql-server
kubectl delete service postgres-server
kubectl delete service redis-service
kubectl delete service thrift-server
