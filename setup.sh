#! /usr/bin/env bash

mkdir -p /home/igor/ct-taiga/data/logs
mkdir -p /home/igor/ct-taiga/data/postgres
# common host volume for visibility of /var/run/postgres from postgres and taiga-back

# common host logs volume for taiga-back and taiga-front
docker volume create ct-taiga-volume
docker volume create ct-taiga-psql-volume

docker run -d --name postgres -v /home/igor/ct-taiga/data/postgres:/var/lib/postgresql/data -v ct-taiga-psql-volume:/var/run postgres
# postgres needs some time to startup
sleep 5

docker run -d --name ct-taiga-back -p 222:22 -p 8000:8000 --link postgres:postgres -v ct-taiga-psql-volume:/var/run -v ct-taiga-volume:/home/taiga -v /home/igor/ct-taiga/data/logs:/home/taiga/logs ct-taiga-back
# docker run -d --name taiga-front -p 80:80 --link taiga-back:taiga-back --volumes-from taiga-back mytaiga/taiga-front

docker run -it --link postgres:postgres --rm postgres sh -c "su postgres --command 'createuser -h "'$POSTGRES_PORT_5432_TCP_ADDR'" -p "'$POSTGRES_PORT_5432_TCP_PORT'" -d -r -s taiga'"
docker run -it --link postgres:postgres --rm postgres sh -c "su postgres --command 'createdb -h "'$POSTGRES_PORT_5432_TCP_ADDR'" -p "'$POSTGRES_PORT_5432_TCP_PORT'" -O taiga taiga'";
docker run -it --rm --link postgres:postgres -v psql-volume:/var/run ct-taiga-back bash -c "source /usr/local/bin/virtualenvwrapper.sh; workon taiga; ./migrate.sh"
