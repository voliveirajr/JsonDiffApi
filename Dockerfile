FROM ubuntu

# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update

# Install Python
RUN apt-get install -y python-dev python-pip

RUN pip install uwsgi

COPY . /app

# Install app requirements
RUN pip install -r app/requirements.txt

# Create app directory
#ADD . /JsonDiffApi

# Set the default directory for our environment
ENV HOME /app
ENV PYTHONPATH /app
WORKDIR /app

# Expose port 8080 for uwsgi
#EXPOSE 8080
