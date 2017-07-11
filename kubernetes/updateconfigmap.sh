#!/usr/bin/env bash

CLIENT_YML=deployments/client.yml

usage()
{
	echo "Usage: ./updateconfigmap.sh -f <configmap_file_path>" 1>&2
	exit 1;
}

while getopts ":f:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

echo $f
if [ -z "${f}" ]; then
    usage
fi

kubectl replace  -f $f
if [ $? -eq 0 ]; then
	REPLICA=$(kubectl get deployment netsil-client --output=jsonpath={.status.replicas})
	echo "deleting old deployment.."
	kubectl scale deploy/netsil-client --replicas=0
	echo "creating new deployment.."
	kubectl scale deploy/netsil-client --replicas=$((REPLICA))
	echo "configmap updated successfully."
else
	echo "something went wrong.."
fi
