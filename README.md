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