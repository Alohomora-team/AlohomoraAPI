FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1


RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY ./app /app


