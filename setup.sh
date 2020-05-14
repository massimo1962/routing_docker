#! /bin/bash

docker build -t "routing:1.1.2" .

docker run -d --name routing-service2 -p 9999:80 routing:1.1.2

docker exec -it routing-service2 python3 /var/www/eidaws/routing/1/data/updateAll.py

docker restart routing-service2
