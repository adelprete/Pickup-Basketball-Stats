# Use an official Python runtime as a parent image
FROM python:3

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Migrate
RUN python3 /app/manage.py migrate

# Copy dummy database
#COPY dump_db.sql /tmp/dump_db.sql

# Install nginx
RUN apt-get update
RUN apt-get install -y nginx
RUN rm /etc/nginx/sites-enabled/default
COPY SaturdayBasketballDocker.conf /etc/nginx/sites-enabled/SaturdayBasketballDocker.conf
RUN service nginx reload
RUN service nginx restart
CMD ["nginx", "-g", "daemon off;"]
