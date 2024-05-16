# syntax=docker/dockerfile:1

# base image -> step1
FROM python:3.12.3-slim-bookworm

# where do i need to run my code -> step 2
WORKDIR /xbank


RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set MySQL client CFLAGS and LDFLAGS
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# code the code that i have written inside the container
COPY requirements.txt requirements.txt

# run my code
RUN pip install mysqlclient
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "run.py"]

# build an image for my need basis a base image 
# run the docker container based on the image i created 
# Process of creating an image is called building an image -> 
# Running a container

#docker build --tag xbank .
#docker run -d -p 5010:5000 xbank
#docker images
#docker history xbank

#1) build image
#2) create container
#3) Ran it
# a) stop/strat
# b) pause/unpause
# c) kill the container
#4) Remove container
