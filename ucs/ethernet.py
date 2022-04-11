# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects power usage metrics from UCSM
from prometheus_client import Gauge
from . import utils as u

ether_stats_bytes_rx = Gauge('ucs_ether_stats_bytes_rx', 'Ethernet Bytes Total RX',
                             ('domain', 'pc_label', 'pc_name'))
ether_stats_bytes_tx = Gauge('ucs_ether_stats_bytes_tx', 'Ethernet Bytes Total TX',
                             ('domain', 'pc_label', 'pc_name'))

eth_err_labels = list(u.DEFAULT_LABELS.keys())
ucs_eth_err_align = Gauge('ucs_eth_err_align', 'align',
    eth_err_labels)
ucs_eth_err_deferred_tx = Gauge('ucs_eth_err_deferred_tx', 'deferred_tx',
    eth_err_labels)
ucs_eth_err_fcs = Gauge('ucs_eth_err_fcs', 'fcs',
    eth_err_labels)
ucs_eth_err_int_mac_rx = Gauge('ucs_eth_err_int_mac_rx', 'int_mac_rx',
    eth_err_labels)
ucs_eth_err_int_mac_tx = Gauge('ucs_eth_err_int_mac_tx', 'int_mac_tx',
    eth_err_labels)
ucs_eth_err_out_discard = Gauge('ucs_eth_err_out_discard', 'out_discard',
    eth_err_labels)
ucs_eth_err_rcv = Gauge('ucs_eth_err_rcv', 'rcv',
    eth_err_labels)
ucs_eth_err_under_size = Gauge('ucs_eth_err_under_size', 'under_size',
    eth_err_labels)
ucs_eth_err_xmit = Gauge('ucs_eth_err_xmit', 'xmit',
    eth_err_labels)

class Ethernet:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        self.gen_x_metric(stats['EtherRxStats'], ether_stats_bytes_rx)
        self.gen_x_metric(stats['EtherTxStats'], ether_stats_bytes_tx)

        for item in stats['EtherErrStats']:
            labels = dict.fromkeys(eth_err_labels) | {'domain': self.domain}
            pieces = item.dn.split('/')
            if 'chassis' in item.dn:
                (_, labels['chassis'], _, _, _, _) = pieces

            ucs_eth_err_deferred_tx.labels(**labels).set(int(item.deferred_tx))
            ucs_eth_err_fcs.labels(**labels).set(int(item.fcs))
            ucs_eth_err_int_mac_rx.labels(**labels).set(int(item.int_mac_rx))
            ucs_eth_err_int_mac_tx.labels(**labels).set(int(item.int_mac_tx))
            ucs_eth_err_out_discard.labels(**labels).set(int(item.out_discard))
            ucs_eth_err_rcv.labels(**labels).set(int(item.rcv))
            ucs_eth_err_under_size.labels(**labels).set(int(item.under_size))
            ucs_eth_err_xmit.labels(**labels).set(int(item.xmit))

    def gen_x_metric(self, items, metric):
        for item in items:
            pieces = item.dn.split('/')
            if pieces[0] != 'fabric':
                continue
            (_, _, pc_label, pc_name, _) = pieces
            metric.labels(self.domain, pc_label, pc_name).set(int(item.total_bytes))