#MathematicalService

Application depends on cache to run, which depends on the monitoring yaml file. So run that yaml file before running the service

```docker-compose -f docker-compose-monitoring.yaml --env-file=.env.dev --build up```

for running the application use below command

```docker-compose --env-file=.env.dev --build up```

for running docker-compose as daemon add ```-d``` option. for example ```docker-compose -d up```

for modifying any configs/envs modify ```.env.dev``` file as needed

Couple of dashboards for monitoring are added inside ```/grafana``` folder at root level as json files.
They can be easily imported from grafana. 
For reference: https://grafana.com/docs/grafana/latest/dashboards/export-import/

