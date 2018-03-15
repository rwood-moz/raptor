#!/usr/bin/env python

# simple local server on port 8000, to demonstrate
# receiving hero element timing results from a web extension

import BaseHTTPServer
import json
import os

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        # get handler, received request for test settings from web ext runner
        self.send_response(200)
        validFiles = ['raptor-firefox-tp7.json', 
                      'raptor-chrome-tp7.json',
                      'raptor-speedometer.json'];
        head, tail = os.path.split(self.path)
        if tail in validFiles:
            print('reading test settings from ' + tail)
            try:
                with open(tail) as json_settings:
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(json.load(json_settings)))
                    self.wfile.close()
                    print('sent test settings to web ext runner')
            except Exception as ex:
                print('control server exception')
                print(ex)
        else:
            print('received request for unknown file: ' + self.path)

    def do_POST(self):
        # post handler, received results from web ext runner
        print "received test results"
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)
        print data

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print "Raptor control server running on port 8000..."
    httpd.serve_forever()

if __name__ == "__main__":
    run()
