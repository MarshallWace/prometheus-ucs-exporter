# Collects power usage metrics from UCS
from prometheus_client import Gauge
from . import utils as u

compute_mb_consumed_power = Gauge('ucs_compute_mb_consumed_power',
                                  'Power consumed by compute MB',
                                  list(u.DEFAULT_LABELS.keys()))
compute_mb_input_current = Gauge('ucs_compute_mb_input_current',
                                 'Input current to compute MB',
                                 list(u.DEFAULT_LABELS.keys()))
compute_mb_input_voltage = Gauge('ucs_compute_mb_input_voltage',
                                 'Input voltage to compute MB',
                                 list(u.DEFAULT_LABELS.keys()))

class Power:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['ComputeMbPowerStats']:
            labels = u.setup_labels(self.domain)
            if 'chassis' in item.dn:
                (_, labels['chassis'], labels['blade'], _, _) = \
                    item.dn.split("/")
            else:
                (_, labels['rack'], _, _) = item.dn.split("/")
            compute_mb_consumed_power.labels(**labels).set(
                float(item.consumed_power))
            compute_mb_input_current.labels(**labels).set(float(
                item.input_current))
            compute_mb_input_voltage.labels(**labels).set(float(
                item.input_voltage))
        return