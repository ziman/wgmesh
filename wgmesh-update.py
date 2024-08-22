#!/usr/bin/env python3

import urllib.request
import argparse
import subprocess

Args = argparse.Namespace


def system(cmd: list[str]) -> str:
    p = subprocess.run(cmd, check=True, capture_output=True)
    return p.stdout.decode('ascii')


def update_endpoints(args: Args) -> None:
    peers = {
        pk
        for pk in system(['wg', 'show', args.iface, 'peers']).split()
        if pk
    }

    info = urllib.request.urlopen(args.url_hub).read().decode('ascii')
    for line in info.split('\n'):
        if not line:
            continue

        pubkey, endpoint = line.split('\t')
        if pubkey in peers:
            system(['wg', 'set', args.iface, 'peer', pubkey, 'endpoint', endpoint])


def main(args: Args) -> None:
    update_endpoints(args)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('iface')
    ap.add_argument('url_hub')
    main(ap.parse_args())
