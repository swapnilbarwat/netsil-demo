import sys
import os
import yaml

# dir = os.path.dirname(__file__)
# filename = os.path.join(dir, '../kubeernetes/deployments/client.yml')
# configmap = os.path.join(dir, '../kubeernetes/configmap.yml')
configmap="../kubeernetes/configmap.yml"
filename="../kubeernetes/deployments/client.yml"

os.system("kubectl replace  -f " + configmap)
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
