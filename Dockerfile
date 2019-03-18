FROM ubuntu:18.04

RUN apt -y update && \
    apt -y install python3-pip

RUN mkdir /app
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

WORKDIR /app

CMD gunicorn app:app -b 127.0.0.1:8080
