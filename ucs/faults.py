# Collects fault metrics from UCS
from collections import defaultdict
from prometheus_client import Gauge

ucs_faults_total = Gauge('ucs_faults_total', 'Faults', ['domain', 'type', 'severity'])

class Faults:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        faults = stats['FaultInst']
        metrics = defaultdict(list)

        for fault in faults: metrics[fault.type + fault.severity].append(fault)
        fault_groups = [{ 'group': k, 'occurrences': v } for k,v in metrics.items()]

        for fault_group in fault_groups:
            cause_type = fault_group['occurrences'][0].type
            severity = fault_group['occurrences'][0].severity
            occurrences = sum([int(f.occur) for f in fault_group['occurrences']])
            labels = {'domain': self.domain, 'type': cause_type, 'severity': severity }
            ucs_faults_total.labels(**labels).set(occurrences)
        return