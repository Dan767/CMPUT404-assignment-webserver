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

#valid_host = []
#redirect_host = []

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        inData = self.data.split()
        if inData[0] != b'GET':
            self.send_405()
            
        #elif 
        #self.request.sendall(bytearray("OK",'utf-8'))

    def send_405(self):
        response = 'HTTP/1.1 405 Method Not Allowed\r\nContent-type:text/html\r\nContent-length:0\r\nConnection: close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))

    def send_301(self,new):
        response = 'HTTP/1.1 301 Redirect\r\nContent-type:text/html\r\nContent-length:'+length+'\r\nConnection: close\r\n'+new+'\r\n\r\n'

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
