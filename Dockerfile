FROM ubuntu:18.04

RUN apt -y update && \
    apt -y install python3-pip

RUN mkdir /app
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

EXPOSE 5000
WORKDIR /app

# HEALTHCHECK CMD curl --fail http://localhost:8080/metrics/ || exit 1

CMD python3 ./app.py
