# SPDX-FileCopyrightText: 2022 2022 Marshall Wace <opensource@mwam.com>
#
# SPDX-License-Identifier: GPL-3.0-only

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
