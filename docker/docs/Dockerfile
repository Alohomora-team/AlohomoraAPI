FROM python:3.6-alpine


WORKDIR /home

COPY docker/docs/requirements.txt . 

RUN pip3 install --no-cache -r requirements.txt

COPY docs/ .

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8080"]
