# prometheus-ucs-exporter

## Overview

Use metrics from the UCS API to export relevant metrics to Prometheus

## Installation

Install requirements

```
pip3 install -r requirements.txt
```

Make the credentials to use are available in the environment, something like:

```
export PROM_UCS_USERNAME='ucs-mydomain\username'
export PROM_UCS_PASSWORD='passw0rd'
export PROM_UCS_HOST='my-host.example.com'
export PROM_UCS_LISTEN='0.0.0.0' # This default is 127.0.0.1
```

Run the app with:

```
./app.py
```

For production, you probably want to use a real uwsgi server
