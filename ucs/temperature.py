# Collects power usage metrics from UCS
from prometheus_client import Gauge
from . import utils as u

processor_env_stats = Gauge('ucs_server_temperature',
                            'Processor Environmental Stats in Celsius',
                            list(u.DEFAULT_LABELS.keys()) + ['cpu'])

class Temperature:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['ProcessorEnvStats']:
            labels = u.setup_labels(self.domain)
            if 'chassis' in item.dn:
                (_, labels['chassis'], labels['blade'], _, labels['cpu'],
                _) = item.dn.split("/")
            else:
                (_, labels['rack'], _, labels['cpu'], _) = \
                    item.dn.split("/")
            try:
                processor_env_stats.labels(**labels).set(float(item.temperature))
            except Exception as e:
                logging.debug("%s" % labels)
                logging.debug("Passed on exception: %s" % e)
                pass