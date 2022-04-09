# Collects memory error stats metrics from UCS
from prometheus_client import Gauge
from . import utils as u

memory_error_labels = list(u.DEFAULT_LABELS.keys())

address_parity_errors = Gauge('ucs_address_parity_errors',
    'address_parity_errors', memory_error_labels)
address_parity_errors_correctable = Gauge('ucs_address_parity_errors_correctable',
    'address_parity_errors_correctable', memory_error_labels)
address_parity_errors_un_correctable = Gauge('ucs_address_parity_errors_un_correctable',
    'address_parity_errors_un_correctable', memory_error_labels)
dram_write_data_correctable_crc_errors = Gauge('ucs_dram_write_data_correctable_crc_errors',
    'dram_write_data_correctable_crc_errors', memory_error_labels)
dram_write_data_un_correctable_crc_errors = Gauge('ucs_dram_write_data_un_correctable_crc_errors',
    'dram_write_data_un_correctable_crc_errors', memory_error_labels)
ecc_multibit_errors = Gauge('ucs_ecc_multibit_errors',
    'ecc_multibit_errors', memory_error_labels)
ecc_singlebit_errors = Gauge('ucs_ecc_singlebit_errors',
    'ecc_singlebit_errors', memory_error_labels)
mismatch_errors = Gauge('ucs_mismatch_errors',
    'mismatch_errors', memory_error_labels)

class MemError:
    def __init__(self, domain):
        self.domain = domain

    def generate_metrics(self, stats):
        for item in stats['MemoryErrorStats']:
            labels = u.setup_labels(self.domain)
            pieces = item.dn.split('/')
            if 'chassis' in item.dn:
                (_, labels['chassis'], labels['blade'], _, _, _, _) = pieces
            else:
                (_, labels['rack'], _, _, _, _) = pieces
            address_parity_errors.labels(**labels).set(
                int(item.address_parity_errors))
            address_parity_errors_correctable.labels(**labels).set(
                int(item.address_parity_errors_correctable))
            address_parity_errors_un_correctable.labels(**labels).set(
                int(item.address_parity_errors_un_correctable))
            dram_write_data_correctable_crc_errors.labels(**labels).set(
                int(item.dram_write_data_correctable_crc_errors))
            dram_write_data_un_correctable_crc_errors.labels(**labels).set(
                int(item.dram_write_data_un_correctable_crc_errors))
            ecc_multibit_errors.labels(**labels).set(
                int(item.ecc_multibit_errors))
            ecc_singlebit_errors.labels(**labels).set(
                int(item.ecc_singlebit_errors))
            mismatch_errors.labels(**labels).set(
                int(item.mismatch_errors))