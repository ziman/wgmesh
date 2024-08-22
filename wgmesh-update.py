#!/usr/bin/env python3

import urllib.request
import argparse
import subprocess

Args = argparse.Namespace


def system(cmd: list[str]) -> str:
    print(cmd)
    p = subprocess.run(cmd, check=True, capture_output=True)
    return p.stdout.decode('ascii')


def parse_endpoints(blob : str) -> dict[str, str]:
    return dict(
        line.split('\t')
        for line in blob.split('\n')
        if line
    )


def update_endpoints(args: Args) -> None:
    peers = [
        pk
        for pk in system(['wg', 'show', args.iface, 'peers']).split()
        if pk
    ]

    endpoints_hub = parse_endpoints(
        urllib.request.urlopen(args.url_hub).read().decode('ascii')
    )

    endpoints_local = parse_endpoints(
        system(['wg', 'show', 'all', 'endpoints'])
    )

    for peer in peers:
        endpoint_hub = endpoints_hub.get(peer)
        if not endpoint_hub:
            # no info from hub, can't do anything
            continue

        endpoint_local = endpoints_local.get(peer)
        if endpoint_local == endpoint_hub:
            # already up to date
            continue

        # we need to update the endpoint
        system([
            'wg', 'set', args.iface, 'peer', peer, 'endpoint', endpoint_hub
        ])


def main(args: Args) -> None:
    update_endpoints(args)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('iface')
    ap.add_argument('url_hub')
    main(ap.parse_args())
