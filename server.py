#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


redirect_lookups = [b'127.0.0.1:8080/deep',b'127.0.0.1:8080']
loc_lookups = ['127.0.0.1:8080/','127.0.0.1:8080/deep/']
file_lookups = ['127.0.0.1:8080/index.html','127.0.0.1:8080/base.css','127.0.0.1:8080/deep/index.html','127.0.0.1:8080/deep/base.css']

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        inData = self.data.split()
        print(inData)
        req_url = inData[inData.index(b'Host:')+1]
        if inData[0] != b'GET':
            fxn = '405 Sent!'
            self.send_405()
        elif req_url in redirect_lookups:
            fxn = '301 Sent!'
            self.send_301(req_url)
        elif req_url in loc_lookups:
            fxn = '200 Sent!'
            self.send_200_loc(req_url)
        elif req_url in file_lookups:
            fxn = '200 Sent!'
            self.send_200_file(req_url)
        else:
            fxn = '400 Sent!'
            self.send_400()
        print(fxn)

    def send_400(self):
        response = 'HTTP/1.1 400 Bad Request\r\nContent-type:text/html\r\nContent-length:0\r\nConnection: close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))
        
    def send_405(self):
        response = 'HTTP/1.1 405 Method Not Allowed\r\nContent-type:text/html\r\nContent-length:0\r\nConnection: close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))

    def send_301(self,req):
        new = req+b'/'
        response = 'HTTP/1.1 301 Moved Permanently\r\nLocation:'+str(new)+'\r\nContent-type:text/html\r\nContent-length:0\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
