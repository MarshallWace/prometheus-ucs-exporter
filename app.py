#!/usr/bin/env python3

from flask import Flask
from flask import Response
from humanfriendly import parse_timespan
import sys
import os
import threading
from prometheus_client import Gauge, generate_latest
from prometheus_client import start_http_server
import time
from ucsmsdk.ucshandle import UcsHandle
if 'PROM_UCS_LISTEN' in os.environ:
    listen = os.environ.get('PROM_UCS_LISTEN')
else:
    listen = '127.0.0.1'


def get_required_env(env_name):
    """Look up and return an environmental variable, or fail if not found."""
    if env_name not in os.environ:
        sys.stderr.write((
            "Oops, looks like you haven't set %s, please do that"
            " and then try running the script again\n"
        ) % env_name)
        sys.exit(2)
    else:
        return os.environ[env_name]


username = get_required_env('PROM_UCS_USERNAME')
password = get_required_env('PROM_UCS_PASSWORD')
host = get_required_env('PROM_UCS_HOST')

collect_increment = os.environ.get('PROM_UCS_INCR', '60s')
collect_increment_seconds = parse_timespan(collect_increment)


# Set up responder API
app = Flask(__name__)

# Set up prometheus stuff here
default_labels = {
    'host': host,
    'rack': 'null',
    'chassis': 'null',
    'blade': 'null'
}
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
processor_env_stats = Gauge(
    'processor_env_stats', 'Processor Environmental Stats in Celcious',
    list(default_labels.keys()) + ['cpu'])
vnic_stats_rx = Gauge(
    'vnic_stats_rx', 'HBA Statisitics for VNIC in Bytes Recieved',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
vnic_stats_tx = Gauge(
    'vnic_stats_tx', 'HBA Statisitics for VNIC in Bytes Transmitted',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
vnic_stats_packets_rx = Gauge(
    'vnic_stats_packets_rx', 'HBA Statisitics for VNIC in Packets Recieved',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
vnic_stats_packets_tx = Gauge(
    'vnic_stats_packets_tx', 'HBA Statisitics for VNIC in Packets Transmitted',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
vnic_stats_errors_rx = Gauge(
    'vnic_stats_errors_rx', 'HBA Statisitics for VNIC in Errors Recieved',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
vnic_stats_errors_tx = Gauge(
    'vnic_stats_errors_tx', 'HBA Statisitics for VNIC in Errors Transmitted',
    list(default_labels.keys()) + ['host_fc', 'adaptor'])
compute_mb_consumed_power = Gauge(
    'compute_mb_consumed_power', 'Power consumed by compute MB',
    list(default_labels.keys()))
compute_mb_input_current = Gauge(
    'compute_mb_input_current', 'Input current to compute MB',
    list(default_labels.keys()))
compute_mb_input_voltage = Gauge(
    'compute_mb_input_voltage', 'Input voltage to compute MB',
    list(default_labels.keys()))

ether_stats_bytes_rx = Gauge(
    'ether_stats_bytes_rx', 'Ethernet Bytes Total RX',
    ('host', 'pc_label', 'pc_name')
)
ether_stats_bytes_tx = Gauge(
    'ether_stats_bytes_tx', 'Ethernet Bytes Total TX',
    ('host', 'pc_label', 'pc_name')
)


@app.before_first_request
def activate_job():
    def run_job():
        handle = UcsHandle(host, username, password)
        handle.login()

        while True:
            print("Collecting new metrics")

            labels = default_labels.copy()
            for item in handle.query_classid('computeMbPowerStats'):
                if 'chassis' in item.dn:
                    (_, labels['chassis'], labels['blade'], _, _) = \
                        item.dn.split("/")
                else:
                    (_, labels['rack'], _, _) = item.dn.split("/")
                compute_mb_consumed_power.labels(**labels).set(
                    float(item.consumed_power))
                compute_mb_input_current.labels(**labels).set(
                    float(item.input_current))
                compute_mb_input_voltage.labels(**labels).set(
                    float(item.input_voltage))

            labels = default_labels.copy()
            for item in handle.query_classid('ProcessorEnvStats'):
                if 'chassis' in item.dn:
                    (_, labels['chassis'], labels['blade'], _, labels['cpu'],
                     _) = item.dn.split("/")
                else:
                    (_, labels['rack'], _, labels['cpu'], _) = \
                        item.dn.split("/")
                processor_env_stats.labels(**labels).set(
                    float(item.temperature))

            labels = default_labels.copy()
            for item in handle.query_classid('adaptorVnicStats'):
                if 'chassis' in item.dn:
                    (_, labels['chassis'], labels['blade'],
                     labels['adaptor'], labels['host_fc'], _) = \
                        item.dn.split("/")
                else:
                    (_, labels['rack'], labels['adaptor'], labels['host_fc'],
                     _) = item.dn.split("/")
                vnic_stats_rx.labels(**labels).set(int(item.bytes_rx))
                vnic_stats_tx.labels(**labels).set(int(item.bytes_tx))
                vnic_stats_packets_rx.labels(**labels).set(int(
                    item.packets_rx))
                vnic_stats_packets_tx.labels(**labels).set(int(
                    item.packets_tx))
                vnic_stats_errors_rx.labels(**labels).set(int(
                    item.errors_rx))
                vnic_stats_errors_tx.labels(**labels).set(int(
                    item.errors_tx))

            for item in handle.query_classid('etherRxStats'):
                pieces = item.dn.split('/')

                # We just care about fabric right now
                if pieces[0] != 'fabric':
                    continue

                (_, _, pc_label, pc_name, _) = pieces
                ether_stats_bytes_rx.labels(
                    host, pc_label, pc_name).set(int(item.total_bytes))

            for item in handle.query_classid('etherTxStats'):
                pieces = item.dn.split('/')

                # We just care about fabric right now
                if pieces[0] != 'fabric':
                    continue

                (_, _, pc_label, pc_name, _) = pieces
                ether_stats_bytes_tx.labels(
                    host, pc_label, pc_name).set(int(item.total_bytes))

            # Sleep for increment
            time.sleep(int(collect_increment_seconds))

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/metrics/')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    activate_job()
    start_http_server(8080)
