FROM python:3.6-alpine

WORKDIR /home

COPY docker/bot/requirements.txt .

RUN apk add --update \
        libressl-dev \
        musl-dev \
        libffi-dev \
        g++ 

RUN pip3 install --no-cache-dir -r requirements.txt

COPY bot/ .

CMD ["python3", "main.py"]
