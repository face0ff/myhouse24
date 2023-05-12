# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /myhouse/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
# copy project
COPY . .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y locales

# Locale
RUN sed -i -e \
  's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
   && locale-gen

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
