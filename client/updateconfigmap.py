import sys
import os
import yaml

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../kubeernetes/deployments/client.yml')

os.system("kubectl replace configmap http-error-workload --from-file requests.json")
stream = open(filename, "w")
deployFile = yaml.load_all(stream)
originalReplicaCount= deployFile["spec"]["replicas"]
deployFile['spec']['replicas'] = 0
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)

os.system("kubectl apply -f " + filename)

deployFile['spec']['replicas'] = originalReplicaCount
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)