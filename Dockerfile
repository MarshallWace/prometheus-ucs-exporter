FROM python:3.9-alpine3.15
RUN mkdir /app
COPY ./requirements.txt /app/
RUN pip3 install -r /app/requirements.txt pip setuptools --default-timeout=100
COPY ./app.py /app/app.py
COPY ./scripts/explore.py /app/explore.py
COPY ./ucs /app/ucs
WORKDIR /app
ENV DESCRIPTION="prometheus-ucs-exporter exports metrics in Prometheus format\
from Cisco Unified Computing System Manager and is maintained by Marshall Wace."
LABEL description="$DESCRIPTION" \
      maintainer="MWAM Infra Team" \
      io.k8s.description="$DESCRIPTION"
# create dir, group and user for easy use by non-root apps
RUN addgroup -S appuser && \
    adduser -u 1337 -S -s /bin/false -h /app -G appuser appuser && \
    chown -R appuser:appuser .
USER appuser
CMD uvicorn app:app --host ${LISTEN_ADDRESS:-"0.0.0.0"} --port ${PORT:-80}
