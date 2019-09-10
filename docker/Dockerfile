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

ENTRYPOINT ["python3", "manage.py"]

CMD ["runserver", "0:8000"]
