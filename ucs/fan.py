# Collects fan speed stats from UCSM
from prometheus_client import Gauge
from . import utils as u

fan_speed = Gauge('ucs_fan_speed', 'Fan speed',
                  ('domain', 'chassis', 'fan_module', 'fan_name'))

class Fan:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['EquipmentFanStats']:
            (_, chassis, fan_module, fan_name, _) = item.dn.split('/')
            fan_speed.labels(self.domain, chassis, fan_module,
                                        fan_name).set(int(item.speed))