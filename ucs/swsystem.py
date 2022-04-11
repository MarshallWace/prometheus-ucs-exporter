# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

# Collects Software System metrics from UCS
from prometheus_client import Gauge
from . import utils as u

cpu_load = Gauge('ucs_cpu_load', 'CPU load', ('domain', 'switch'))
mem_available = Gauge('ucs_mem_available', 'Memory available', ('domain', 'switch'))
mem_cached = Gauge('ucs_mem_cached', 'Memory cached', ('domain', 'switch'))
kernel_mem_free = Gauge('ucs_kernel_mem_free', 'Kernel memory free', ('domain', 'switch'))
kernel_mem_total = Gauge('ucs_kernel_mem_total', 'Kernel memory total', ('domain', 'switch'))

class SwSystem:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['SwSystemStats']:
            (_, switch, _) = item.dn.split('/')
            cpu_load.labels(self.domain, switch).set(float(item.load))
            mem_available.labels(self.domain, switch).set(int(item.mem_available))
            mem_cached.labels(self.domain, switch).set(int(item.mem_cached))
            kernel_mem_total.labels(self.domain, switch).set(int(item.kernel_mem_total))
            kernel_mem_free.labels(self.domain, switch).set(int(item.kernel_mem_free))