FROM python:3.10
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
# Set the working directory in the container

COPY pg_hba.conf /etc/postgresql/15/main
COPY postgresql.conf /etc/postgresql/15/main
WORKDIR backend

COPY  backend/requirement.txt .


COPY script.sh /


RUN ls && pip install --no-cache-dir -r requirement.txt

RUN chmod 777 /script.sh

# Run migrations and start the Django server
CMD ["sh","-c","/script.sh"]