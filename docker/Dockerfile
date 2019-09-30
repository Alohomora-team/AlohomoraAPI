FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/lib/python3.7/site-packages

WORKDIR /home

RUN apk add --update --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    py3-numpy \
    py3-scipy

COPY docker/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENTRYPOINT ["python3", "manage.py"]

CMD ["runserver", "0:8000"]
