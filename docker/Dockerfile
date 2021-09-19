FROM python:3.8-slim-buster

WORKDIR app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc redis-server\
    && pip install psycopg2


ARG PORT
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt install -y python3-dev python3-pip


RUN pip3 install setuptools

COPY requirements.txt /app


RUN pip install -r requirements.txt


