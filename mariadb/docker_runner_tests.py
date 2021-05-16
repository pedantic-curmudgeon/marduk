# Try running with this as the data mount: /home/raeganbarker/docker/mariadb1

# docker run -p 127.0.0.1:3306:3306 --name some-mariadb -v /home/raeganbarker/docker/data/mariadb1:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=main -d mariadb:10.5.9

# Reference from MariaDB Docker page:
# docker run --name some-mariadb -v /my/own/datadir:/var/lib/mysql -e MARIADB_ROOT_PASSWORD=my-secret-pw -d mariadb:tag

# The above allows us to point to a specific location for all the database data to be written to.

# From there, we can zip it, back it up, migrate it, etc (With the right permissions, of course.)
