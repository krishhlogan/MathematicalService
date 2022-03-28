#MathematicalService

Application depends on cache to run, which depends on the monitoring yaml file. So run that yaml file before running the service

```docker-compose -f docker-compose-monitoring.yaml --env-file=.env.dev --build up```

for running the application use below command

```docker-compose --env-file=.env.dev --build up```



for modifying any configs/envs modify ```.env.dev``` file as needed
