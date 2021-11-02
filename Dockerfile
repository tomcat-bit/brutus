FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./wait-for-it.sh ./wait-for-it.sh

RUN apk update
RUN apk upgrade
RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev \
	&& pip install -r /requirements.txt
#RUN ./wait_for_psql.sh

# Remove dependencies
RUN mkdir /app
WORKDIR /app
COPY ./app /app

COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh
