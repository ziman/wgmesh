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

            self.send_response(200, 'OK')
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(wg.stdout)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((args.addr, args.port), Handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('iface')
    ap.add_argument('addr')
    ap.add_argument('--port', type=int, default=4137)
    main(ap.parse_args())
