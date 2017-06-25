import sys
import os
import yaml

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../kubeernetes/deployments/client.yml')

os.system("kubectl update configmap http-error-workload --from-file requests.json")
stream = open(filename, "w")
deployFile = yaml.load_all(stream)
originalReplicaCount= deployFile["spec"]["replicas"]
deployFile['spec']['replicas'] = 0
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)

print("Scaling down to 0")
os.system("kubectl apply -f " + filename)

deployFile['spec']['replicas'] = originalReplicaCount
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)

print("Scaling down to original value" + originalReplicaCount)
os.system("kubectl apply -f " + filename)
