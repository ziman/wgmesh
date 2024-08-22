#!/usr/bin/env python3

import urllib.request
import argparse
import subprocess
import logging

Args = argparse.Namespace
log = logging.getLogger('wgmesh-update')

def system(cmd: list[str]) -> str:
    log.debug('%s', ' '.join(cmd))
    p = subprocess.run(cmd, check=True, capture_output=True)
    return p.stdout.decode('ascii')


def parse_endpoints(blob: str) -> dict[str, str]:
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
        system(['wg', 'show', args.iface, 'endpoints'])
    )

    for peer in peers:
        endpoint_hub = endpoints_hub.get(peer)
        if not endpoint_hub:
            # no info from hub, can't do anything
            log.debug('peer %s is not known by the hub', peer)
            continue

        endpoint_local = endpoints_local.get(peer)
        if endpoint_local == endpoint_hub:
            # already up to date
            log.debug('peer %s up to date at %s', peer, endpoint_local)
            continue

        # we need to update the endpoint
        log.info(
            'setting endpoint of %s from %s to %s',
            peer, endpoint_local, endpoint_hub,
        )
        system([
            'wg', 'set', args.iface, 'peer', peer, 'endpoint', endpoint_hub
        ])


def main(args: Args) -> None:
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO
    )
    update_endpoints(args)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('iface')
    ap.add_argument('url_hub')
    ap.add_argument('-v', '--verbose', action='store_true')
    main(ap.parse_args())
