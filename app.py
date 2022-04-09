#!/usr/bin/env python3

from fastapi import BackgroundTasks, FastAPI, Query, Response
import logging
import sys
import os
from prometheus_client import Counter, Gauge, generate_latest
from ucsmsdk.ucshandle import UcsHandle
from starlette_exporter import PrometheusMiddleware
from ucs.computecapacity import ComputeCapacity
from ucs.ethernet import Ethernet
from ucs.fan import Fan
from ucs.faults import Faults
from ucs.fibrechannel import FibreChannel
from ucs.memerror import MemError
from ucs.power import Power
from ucs.swsystem import SwSystem
from ucs.temperature import Temperature
from ucs.vnic import Vnic

logger = logging.getLogger()
logger.setLevel(logging.INFO)

username = get_required_env('PROM_UCS_USERNAME')
password = get_required_env('PROM_UCS_PASSWORD')

app = FastAPI(
    title="ucs-exporter",
    description="Prometheus exporter for Cisco UCSM.",
    openapi_tags=[
        {"name": "healthz", "description": "Endpoints for checking health",},
        {"name": "metrics", "description": "Endpoints for fetching metrics",},
    ],
)

app.add_middleware(PrometheusMiddleware)

def get_required_env(env_name):
    """Look up and return an environmental variable, or fail if not found."""
    if env_name not in os.environ:
        sys.stderr.write(
            ("Oops, looks like you haven't set %s, please do that"
             " and then try running the script again\n") % env_name)
        sys.exit(2)
    else:
        return os.environ[env_name]

failure_metric = Counter("ucs_exporter_failure", "Failure counter indicating issues")

ready_domains = {}

@app.get(
    "/healthz",
    tags=["health"],
    description="Health check endpoint, returns 'OK' when healthy",
)
async def healthz():
    return "OK"

@app.get(
    "/metrics",
    tags=["metrics"],
    description="Prometheus metrics endpoint",
    responses={
        200: {
            "description": "Successful response for UCSM request. The data comes from UCSM.",
            "content": {
                "text/plain": {
                    "example": {
                        'ucs_eth_err_xmit{blade="None",chassis="chassis-1",domain="domainname",pc_label="A",pc_name="pc-11",port="port-4",rack="None",slot="slot-1",switch="switch-A"} 0.0'
                        '\nucs_eth_err_xmit{blade="None",chassis="chassis-1",domain="domainname",pc_label="A",pc_name="pc-11",port="port-4",rack="None",slot="slot-2",switch="switch-A"} 0.0'
                    }
                }
            }
        }
    }
)
async def metrics(
    response: Response,
    background_tasks: BackgroundTasks,
    domain: str = Query(None, title='The UCSM domain'),
):
    # We fetch the latest metrics in the background since the UCSM API
    # is slow to respond.
    background_tasks.add_task(fetch_metrics, domain)
    # Return a 503 Service Unavailable if the metrics haven't been scraped
    # yet for this domain to prevent drops in metrics during deployment.
    if ready_domains.get(domain, False):
        return Response(content=generate_latest(), status_code=200)
    else:
        return Response(content=f"Not yet scraped {domain}...", status_code=503)


def fetch_metrics(domain):
    try:
        handle = UcsHandle(domain, username, password)
        handle.login()
        stats = handle.query_classids([
            'ComputeMbPowerStats',
            'ProcessorEnvStats',
            'AdaptorVnicStats',
            'EtherRxStats',
            'EtherTxStats',
            'EquipmentFanStats',
            'SwSystemStats',
            'MemoryErrorStats',
            'FcStats',
            'EtherErrStats',
            'FabricComputeSlotEp',
            'ComputeBlade',
            'ComputeRackUnit',
            'FaultInst',
        ])
        handle.logout()

        ComputeCapacity(domain).generate_metrics(stats)
        Faults(domain).generate_metrics(stats)
        Power(domain).generate_metrics(stats)
        Temperature(domain).generate_metrics(stats)
        Ethernet(domain).generate_metrics(stats)
        Fan(domain).generate_metrics(stats)
        SwSystem(domain).generate_metrics(stats)
        MemError(domain).generate_metrics(stats)
        FibreChannel(domain).generate_metrics(stats)
        Vnic(domain).generate_metrics(stats)
        ready_domains[domain] = True
    except Exception as e:
        logging.error(f"Internal server error {e}")
        failure_metric.inc()
        raise e
