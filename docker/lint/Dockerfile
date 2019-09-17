FROM python:3.6-alpine

WORKDIR /home

COPY docker/lint/requirements.txt .

RUN apk add --update --no-cache \
        build-base

RUN pip3 install --no-cache -r requirements.txt

ENTRYPOINT ["pylint"]
