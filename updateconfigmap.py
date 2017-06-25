import sys
import os
import yaml

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'kubernetes/deployments/client.yml')
configmap = os.path.join(dir, 'kubernetes/configmap.yml')

os.system("kubectl replace  -f " + configmap)
stream = open(filename, "r")
deployFile = yaml.load(stream)
originalReplicaCount= deployFile["spec"]["replicas"]
deployFile['spec']['replicas'] = 0
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)

print("Scaling down to 0")
os.system("kubectl apply -f " + filename)

deployFile['spec']['replicas'] = originalReplicaCount
with  open(filename,"w") as f:
	yaml.dump(deployFile, f)

print("Scaling down to original value" + str(originalReplicaCount))
os.system("kubectl apply -f " + filename)
