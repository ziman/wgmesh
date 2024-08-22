#!/usr/bin/env python3

import logging
import argparse
import subprocess
import http.server
import socketserver

Args = argparse.Namespace

def main(args : Args) -> None:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            wg = subprocess.run(
                ['wg', 'show', args.iface, 'endpoints'],
                check=True, capture_output=True,
            )
            self.wfile.write(wg.stdout)

    with socketserver.TCPServer((args.bind, args.port), Handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('iface')
    ap.add_argument('addr')
    ap.add_argument('port')
    main(ap.parse_args())
