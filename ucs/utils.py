DEFAULT_LABELS = {
    'domain': 'null',
    'rack': 'null',
    'chassis': 'null',
    'blade': 'null'
}

def setup_labels(domain):
    labels = DEFAULT_LABELS.copy()
    labels['domain'] = domain
    return labels
