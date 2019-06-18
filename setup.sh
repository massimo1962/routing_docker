#! /bin/bash

docker build -t "routing:1.1.2" .

docker run -d --name routing-service -p 80:80 routing:1.1.2

docker exec -it routing-service python3 /var/www/eidaws/routing/1/data/updateAll.py

docker restart routing-service