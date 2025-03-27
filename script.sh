# chown -R postgres:postgres /var/lib/postgresql/15/main
# chown -R postgres:postgres /etc/postgresql/15/main
# chown -R postgres:postgres /var/log/postgresql
# service postgresql start && \
ls -la /etc/certs
service postgresql start

sleep 5 


echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"



psql -U $DB_USER -c "create database $DB_NAME;"
if [ $? -eq 0 ];then
    echo "enter"
    psql -U $DB_USER -c "alter user $DB_USER with password '${DB_PASSWORD}'"
fi
python manage.py makemigrations

python manage.py migrate 
watchfiles "hypercorn project.asgi:application --bind 0.0.0.0:8000 --certfile /etc/certs/crt.crt --keyfile /etc/certs/key.key"

# hypercorn  project.asgi:application --bind 0.0.0.0:8000  --certfile /etc/certs/crt.crt --keyfile /etc/certs/key.key