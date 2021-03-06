#!/usr/bin/env python3

# Enables exploring the Cisco UCSM API.
# Example usage:
#   * List available classes:
#     ./scripts/explore.py list-classids
#   * Fetch data for a class:
#     ./scripts/explore.py query-classid ProcessorEnvStats

import sys
import os
import argparse
from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.ucsconstants import NamingId

def parse_args():
    parser = argparse.ArgumentParser(description="Explore UCS API.")
    subparsers = parser.add_subparsers(dest='action', help='sub-command help')
    subparsers.required = True
    classid_parser = subparsers.add_parser('query-classid',
                                           help='Query a given classid')
    classid_parser.add_argument('classid', help='ClassID to look at')

    subparsers.add_parser('list-classids', help='List all classids')

    return parser.parse_args()


def get_required_env(env_name):
    """Look up and return an environmental variable, or fail if not found."""
    if env_name not in os.environ:
        sys.stderr.write((
            "Oops, looks like you haven't set %s, please do that"
            " and then try running the script again\n"
        ) % env_name)
        sys.exit(2)
    else:
        return os.environ[env_name]


def main():
    """
    Explore the UCSM API.

    This script simply calls the UCSM API using credentials set in the
    environment to list available classes or fetch data on a given class.

    Parameters
    ----------
    action : string
        list-classids or query-classid <classid>

    Examples
    --------
    $ explore.py query-classid ProcessorEnvStats
    > prints temperature statistics for servers

    See Also
    --------
    UCSM SDK: https://github.com/CiscoUcs/ucsmsdk
    """
    args = parse_args()

    username = get_required_env('PROM_UCS_USERNAME')
    password = get_required_env('PROM_UCS_PASSWORD')
    domain = get_required_env('PROM_UCS_DOMAIN')

    handle = UcsHandle(domain, username, password)
    handle.login()

    if args.action == 'query-classid':
        for item in handle.query_classid(args.classid):
            print(item)
    elif args.action == 'list-classids':
        for item in NamingId.__dict__.values():
            if not isinstance(item, str):
                continue
            print(item)

    # equipmentFanStats
    handle.logout()
    return 0


if __name__ == "__main__":
    sys.exit(main())
