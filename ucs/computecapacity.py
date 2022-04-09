# ComputeCapacity provides data on equipment available/in-use
# that may be useful for capacity planning.
from prometheus_client import Gauge

default_labels = ["domain","class"]
ucs_servers_total = Gauge('ucs_servers_total',
    'Total servers (blade/rack)', default_labels)
ucs_cpu_cores_total = Gauge('ucs_cpu_cores_total',
    'Total server cpu cores', default_labels)
ucs_cpus_total = Gauge('ucs_cpus_total',
    'Total server cpus', default_labels)
ucs_mem_available_total = Gauge('ucs_mem_available_total',
    'Total memory available', default_labels)
ucs_mem_total = Gauge('ucs_mem_total',
    'Total memory', default_labels)
ucs_slots_total = Gauge('ucs_slots_total',
    'Total slots', default_labels)
ucs_slots_empty = Gauge('ucs_slots_empty',
    'Slots available', default_labels)
ucs_slots_equipped = Gauge('ucs_slots_equipped',
    'Slots in use', default_labels)
class ComputeCapacity:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        self.collect_server_metrics(stats["ComputeBlade"], 'blade')
        self.collect_server_metrics(stats["ComputeRackUnit"], 'rack')
        self.collect_slot_metrics(stats['FabricComputeSlotEp'])
        return

    def collect_slot_metrics(self, slots):
        labels = {'domain': self.domain, 'class': 'blade'}
        ucs_slots_total.labels(**labels).set(len(slots))
        empty_count = len([s for s in slots if s.presence == 'empty'])
        ucs_slots_empty.labels(**labels).set(empty_count)
        used_count = len([s for s in slots if s.presence == 'equipped'])
        ucs_slots_equipped.labels(**labels).set(used_count)

    def collect_server_metrics(self, servers, class_id):
        cores = 0
        cpus = 0
        mem_available = 0
        mem_total = 0
        for server in servers:
            cores += int(server.num_of_cores)
            cpus  += int(server.num_of_cpus)
            mem_available += int(server.available_memory)
            mem_total += int(server.total_memory)
        labels = {'domain': self.domain, 'class': class_id}
        ucs_servers_total.labels(**labels).set(len(servers))
        ucs_cpu_cores_total.labels(**labels).set(cores)
        ucs_cpus_total.labels(**labels).set(cpus)
        ucs_mem_available_total.labels(**labels).set(mem_available)
        ucs_mem_total.labels(**labels).set(mem_total)
        return
