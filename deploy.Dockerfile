FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


WORKDIR /home

RUN apk add --update --no-cache \
    postgresql-dev \
    gcc \
    musl-dev 

COPY docker/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD python3 manage.py runserver 0.0.0.0:$PORT 
