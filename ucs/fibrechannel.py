# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects Fibre Channel metrics from UCS
from prometheus_client import Gauge
from . import utils as u

fc_labels = ('domain', 'pc_name', 'pc_label')
ucs_fc_bytes_rx = Gauge('ucs_fc_bytes_rx', 'Fibre Channel bytes received',
    fc_labels)
ucs_fc_bytes_tx = Gauge('ucs_fc_bytes_tx', 'Fibre Channel bytes transmitted',
    fc_labels)
ucs_fc_packets_rx = Gauge('ucs_fc_packets_rx', 'Fibre Channel packets received',
    fc_labels)
ucs_fc_packets_tx = Gauge('ucs_fc_packets_tx', 'Fibre Channel packets transmitted',
    fc_labels)

class FibreChannel:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['FcStats']:
            fcstatslabels = {'domain': self.domain}
            pieces = item.dn.split('/')
            if pieces[0] != 'fabric':
                continue
            (_, _, fcstatslabels['pc_label'], fcstatslabels['pc_name'], _) = pieces
            ucs_fc_bytes_rx.labels(**fcstatslabels).set(int(item.bytes_rx))
            ucs_fc_bytes_tx.labels(**fcstatslabels).set(int(item.bytes_rx))
            ucs_fc_packets_rx.labels(**fcstatslabels).set(int(item.bytes_rx))
            ucs_fc_packets_tx.labels(**fcstatslabels).set(int(item.bytes_rx))