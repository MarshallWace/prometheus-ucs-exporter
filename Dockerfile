FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app.py /app/main.py
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

ENV LISTEN_PORT 8080
EXPOSE 8080

WORKDIR /app
