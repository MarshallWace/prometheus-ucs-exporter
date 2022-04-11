# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects Virtual Network Interface Card (vNIC) metrics from UCS
from prometheus_client import Gauge
from . import utils as u

vnic_stats_rx = Gauge('ucs_vnic_stats_rx',
                      'HBA Statisitics for VNIC in Bytes Recieved',
                      list(u.DEFAULT_LABELS.keys()))
vnic_stats_tx = Gauge('ucs_vnic_stats_tx',
                      'HBA Statisitics for VNIC in Bytes Transmitted',
                      list(u.DEFAULT_LABELS.keys()))
vnic_stats_packets_rx = Gauge(
    'ucs_vnic_stats_packets_rx', 'HBA Statisitics for VNIC in Packets Recieved',
    list(u.DEFAULT_LABELS.keys()))
vnic_stats_packets_tx = Gauge(
    'ucs_vnic_stats_packets_tx', 'HBA Statisitics for VNIC in Packets Transmitted',
    list(u.DEFAULT_LABELS.keys()))
vnic_stats_errors_rx = Gauge(
    'ucs_vnic_stats_errors_rx', 'HBA Statisitics for VNIC in Errors Recieved',
    list(u.DEFAULT_LABELS.keys()))
vnic_stats_errors_tx = Gauge(
    'ucs_vnic_stats_errors_tx', 'HBA Statisitics for VNIC in Errors Transmitted',
    list(u.DEFAULT_LABELS.keys()))

class Vnic:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['AdaptorVnicStats']:
            labels = u.setup_labels(self.domain)
            if 'chassis' in item.dn:
                (_, labels['chassis'], labels['blade'], _, _, _) = \
                    item.dn.split("/")
            else:
                (_, labels['rack'], _, _, _) = item.dn.split("/")
            vnic_stats_rx.labels(**labels).set(int(item.bytes_rx))
            vnic_stats_tx.labels(**labels).set(int(item.bytes_tx))
            vnic_stats_packets_rx.labels(**labels).set(int(item.packets_rx))
            vnic_stats_packets_tx.labels(**labels).set(int(item.packets_tx))
            vnic_stats_errors_rx.labels(**labels).set(int(item.errors_rx))
            vnic_stats_errors_tx.labels(**labels).set(int(item.errors_tx))
