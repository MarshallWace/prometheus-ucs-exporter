FROM python:3.9-alpine3.15
RUN mkdir /app
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt pip setuptools --default-timeout=100
COPY ./app.py /app/app.py
COPY ./scripts/explore.py /app/explore.py
COPY ./ucs /app/ucs
WORKDIR /app
CMD uvicorn app:app --host ${LISTEN_ADDRESS:-"0.0.0.0"} --port ${PORT:-80}
