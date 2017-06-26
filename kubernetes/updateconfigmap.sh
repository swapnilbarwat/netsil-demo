#!/usr/bin/env bash

CLIENT_YML=deployments/client.yml

usage()
{
	echo "Usage: ./updateconfigmap.sh -f <configmap_file_path>" 1>&2
	exit 1;
}

while getopts ":s:p:" o; do
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

if [ -z "${f}" ]; then
    usage
fi

kubectl replace  -f $f
if [ $OUT -eq 0 ];then
	REPLICA=$(grep -A3 'spec:' $CLIENT_YML | head -n2 | grep -A2 'replicas:' | cut -d':' -f2)
	echo "deleting old deployment.."
	kubectl scale deploy/netsil-client --replicas=0
	echo "creating new deployment.."
	kubectl scale deploy/netsil-client --replicas=$REPLICA	
	echo "configmap updated successfully."
else
	echo "something went wrong.."