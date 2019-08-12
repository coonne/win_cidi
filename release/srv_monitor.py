# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from time import sleep
import cgi
import os
import socket
import datetime
import zipfile
import psutil
import shutil

exists_path = os.path.exists('*')
if not exists_path:
    os.makedirs('*')


class PostHandler(BaseHTTPRequestHandler):
    def _do_post(self):
        print('*')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write(('Client: %sn' % str(self.client_address)).encode('utf-8'))
        self.wfile.write(('User-agent: %sn' & str(self.headers['User-agent'])).encode('utf-8'))
        self.wfile.write(('Path: %sn' % self.path).encode('utf-8'))
        self.wfile.write('Form data: n'.encode('utf-8'))
        getParam = form.keys()

        if "CopyFrom" in getParam:
