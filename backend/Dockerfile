FROM python:3.10
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
# Set the working directory in the container

COPY ../conf/pg_hba.conf /etc/postgresql/15/main

COPY ../conf/postgresql.conf /etc/postgresql/15/main

COPY ../conf/key.key /etc/certs/

COPY ../conf/crt.crt /etc/certs/

RUN ls /etc/certs

WORKDIR backend

COPY  backend/requirement.txt .


RUN  pip install --no-cache-dir -r requirement.txt

COPY script.sh /

RUN chmod 777 /script.sh
# Run migrations and start the Django server
CMD ["sh","-c","/script.sh"]