FROM ubuntu:18.04

RUN apt -y update && \
    apt -y install python3-pip

RUN mkdir /app
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

WORKDIR /app

HEALTHCHECK CMD curl --fail http://localhost:8080/metrics/ || exit 1

CMD gunicorn app:app -b 0.0.0.0:8080
