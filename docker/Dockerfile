FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/lib/python3/dist-packages/

WORKDIR /home

RUN apt-get update && apt-get install -y \  
    python3-numpy \
    python3-scipy

COPY docker/requirements.txt requirements.txt

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENTRYPOINT ["python3", "manage.py"]

CMD ["runserver", "0:8000"]
