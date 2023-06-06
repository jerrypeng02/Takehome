#!/bin/sh
echo "processing pre-setting"

# Start the DB server, create the database, and create the super user
initdb -D ./pgsql/data
pg_ctl -D ./pgsql/data -l logfile start
createdb takehomedb
createuser --superuser user

# Build the docker and run


echo "done process"