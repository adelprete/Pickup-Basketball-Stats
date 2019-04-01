# Use an official Python runtime as a parent image
FROM python:3

# ensure local python is preferred over distribution python
#ENV PATH /usr/local/bin:$PATH
#RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
#RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-10.4 postgresql-client-10.4 postgresql-contrib-10.4

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

#RUN apt-get install postgresql-9.4 -y

#RUN apt install python3-dev postgresql postgresql-contrib python3-psycopg2 libpq-dev

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-10.4`` package when it was ``apt-get installed``
# USER postgres

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
# ENV LANG C.UTF-8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Migrate
RUN ./manage.py migrate

# Copy dummy database
COPY dump_db.sql /tmp/dump_db.sql

# Install nginx
RUN apt-get update
RUN apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
COPY SaturdayBasketballDocker.conf /etc/nginx/sites-enabled/SaturdayBasketballDocker.conf
RUN service nginx reload
RUN service nginx restart
CMD ["nginx", "-g", "daemon off;"]
