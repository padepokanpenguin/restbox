#!/usr/bin/env python3
"""
RestBox Local Server & Built-in CORS Reverse Proxy
- Melayani static files RestBox (HTML, CSS, JS) di port lokal
- Menyediakan reverse proxy endpoint /proxy?url=... untuk mem-bypass CORS browser 100%
- Mendukung GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- Mendukung HTTPS dengan self-signed cert (local development)
- Otomatis melakukan dekompresi gzip/deflate agar response mudah dibaca browser
"""

import os
import sys
import gzip
import zlib
import ssl
import urllib.request
import urllib.error
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8000
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'restbox')
if not os.path.isdir(BASE_DIR):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Hop-by-hop headers yang tidak boleh di-forward
HOP_BY_HOP = {
    'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
    'te', 'trailers', 'transfer-encoding', 'upgrade', 'host', 'content-length'
}

# SSL context yang toleran terhadap self-signed certificates (khas local dev)
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

class RestBoxHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Expose-Headers', '*')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            self.send_error(405, "Method Not Allowed")

    def do_PUT(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            self.send_error(405, "Method Not Allowed")

    def do_DELETE(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            self.send_error(405, "Method Not Allowed")

    def do_PATCH(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            self.send_error(405, "Method Not Allowed")

    def do_HEAD(self):
        if self.path.startswith('/proxy'):
            self.handle_proxy()
        else:
            super().do_HEAD()

    def handle_proxy(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # Health/Ping check untuk deteksi otomatis oleh frontend RestBox
        if 'ping' in params:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","proxy":true,"service":"restbox-cors-proxy"}')
            return

        target_url = params.get('url', [None])[0]
        if not target_url:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":"Missing query parameter: url"}')
            return

        # Pastikan URL memiliki skema http/https
        if not target_url.startswith('http://') and not target_url.startswith('https://'):
            target_url = 'https://' + target_url

        # Baca request body jika ada (POST/PUT/PATCH)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Teruskan request headers kecuali hop-by-hop
        forward_headers = {}
        for key, value in self.headers.items():
            if key.lower() not in HOP_BY_HOP:
                forward_headers[key] = value

        req = urllib.request.Request(
            target_url,
            data=body,
            headers=forward_headers,
            method=self.command
        )

        try:
            with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
                resp_status = resp.status
                resp_headers = resp.getheaders()
                resp_body = resp.read()
                self._send_proxy_response(resp_status, resp_headers, resp_body)

        except urllib.error.HTTPError as e:
            # Tetap teruskan status error dari server target (400, 401, 404, 500, dll)
            resp_headers = e.headers.items() if hasattr(e.headers, 'items') else []
            self._send_proxy_response(e.code, resp_headers, e.read())

        except urllib.error.URLError as e:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_msg = f'{{"error":"Proxy Forwarding Error","reason":"{str(e.reason)}","target":"{target_url}"}}'
            self.wfile.write(err_msg.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err_msg = f'{{"error":"Internal Proxy Error","message":"{str(e)}"}}'
            self.wfile.write(err_msg.encode('utf-8'))

    def _send_proxy_response(self, status, headers, body):
        content_encoding = None
        filtered_headers = []

        for h_name, h_val in headers:
            h_lower = h_name.lower()
            if h_lower == 'content-encoding':
                content_encoding = h_val.lower().strip()
            elif h_lower not in HOP_BY_HOP:
                filtered_headers.append((h_name, h_val))

        # Dekompresi jika server target mengirim gzip/deflate
        if content_encoding == 'gzip' and body:
            try:
                body = gzip.decompress(body)
            except Exception:
                filtered_headers.append(('Content-Encoding', 'gzip'))
        elif content_encoding == 'deflate' and body:
            try:
                body = zlib.decompress(body)
            except Exception:
                try:
                    body = zlib.decompress(body, -zlib.MAX_WBITS)
                except Exception:
                    filtered_headers.append(('Content-Encoding', 'deflate'))

        self.send_response(status)
        for h_name, h_val in filtered_headers:
            self.send_header(h_name, h_val)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RestBoxHandler)
    print("========================================================")
    print("  RestBox - Local Web Server & Built-in CORS Proxy")
    print("========================================================")
    print(f"  Web UI     : http://localhost:{PORT}/")
    print(f"  Directory  : {BASE_DIR}")
    print(f"  CORS Proxy : http://localhost:{PORT}/proxy?url=<target_url>")
    print("--------------------------------------------------------")
    print("  Buka browser di: http://localhost:8000")
    print("  Status     : Ready! Tekan Ctrl+C untuk berhenti.")
    print("========================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dihentikan.")
        httpd.server_close()

if __name__ == '__main__':
    main()
