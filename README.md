#MathematicalService

for running the application use below command

```docker-compose --env-file=.env.dev --build up```

for running docker-compose as daemon add ```-d``` option. for example ```docker-compose -d up```

for modifying any configs/envs modify ```.env.dev``` file as needed

Couple of dashboards for monitoring are added inside ```/grafana``` folder at root level as json files.
They can be easily imported from grafana. 

For reference: https://grafana.com/docs/grafana/latest/dashboards/export-import/

By default, username/password of grafana is admin/admin

Grafana can be accessed from url http://host.docker.internal:3060/

The first time, we would have to add prometheus as data-source.
One can follow below docs to add data-source

https://prometheus.io/docs/visualization/grafana/

# Sample Curls for API

ACKERMANN
```
curl --request POST \
  --url http://host.docker.internal/algorithm/ackermann/ \
  --header 'Content-Type: application/json' \
  --data '{
	"m" : 100,
	"n" : 10
}'
```
FIBONACCI
```
curl --request POST \
  --url http://host.docker.internal/algorithm/fibonacci/ \
  --header 'Content-Type: application/json' \
  --data '{
	"number": 10
}'
```
FACTORIAL
```
curl --request POST \
  --url http://host.docker.internal/algorithm/factorial/ \
  --header 'Content-Type: application/json' \
  --data '{"number":2000}'
```

How to proceed further and deploy them to cloud ?

Push the docker images to any private docker registry.

There are 2 options for redis. One can either go with a fully managed redis service from any cloud service provider or one can choose to deploy and manage their own redis instances.

In first case, we need not push the redis docker image, but instead modify the redis host name, port and password on env. 

If cluster is not available, initial setting up of cluster will be required.
Once we have the kubernetes cluster setup, deployments are much easier.
One have to add the ingress rules, to forward requests to corresponding service.

create deployments and services for API, prometheus, redis (if needed), grafana and redis-exporter in our case.
kubectl command will allow us to create the required deployments and services.

Points to keep in mind

-> To store environment variables,configMap in kubernetes can be used, which will hold the env keys and values. Main advantage of using configMap over env files is that, we dont have to push new changes on env file everytime. we can modify configMap values using kubectl commands

-> Secret or sensitive values are to be stored in secrets, which can be imported to the deployment/services yaml file.

-> Persistent volumes must be allocated outside of the pods/containers, as a restart or deployment would make them lose data.

