FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update
RUN apk upgrade
RUN apk add --update --no-cache postgresql-client

# Add dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev \
	&& pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
