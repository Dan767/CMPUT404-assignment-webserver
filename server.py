#  coding: utf-8 
import socketserver
import os
# Copyright 2020 Daniel Dick
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
# This is derived from the code that is Copyright 2013 Abram Hindle, 
# Eddie Antonio Santos.  This code can be found here:
# 
# http://github.com/abramhindle/CMPUT404-assignment-webserver
#
# Basis for list_dir function derived from answers on stackoverflow
# (modified to suit the scenario). Credit to user badcOre.
#
# https://stackoverflow.com/questions/18510733/python-mapping-all-files-inside-a-folder
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python3 freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

def list_dir(dir_name, traversed = [], results = []): 
    dirs = os.listdir(dir_name)
    results.append(dir_name)
    if dirs:
        for f in dirs:
            new_dir = dir_name + f + '/'
            if os.path.isdir(new_dir) and new_dir not in traversed:
                traversed.append(new_dir)
                list_dir(new_dir, traversed, results)
            else:
                results.append(new_dir[:-1])  
    return results



class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        dirs = []
        dirs = list_dir('www/',[],[])
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        inData = self.data.split()
        #print(inData)
        if (len(inData) < 2):
            return
        req = inData[1]
        req = str(req.decode('UTF-8'))
        req_url = 'www'+ req
        #print("req url = "+str(req_url))
        if inData[0] != b'GET':
            print("405 Sent!")
            self.send_405()
        elif (req_url+'/') in dirs or 'HTTP' in str(inData[1]) or '/' not in str(inData[1]):
            print("301 Sent!")
            self.send_301(req_url)
        elif req_url in dirs and req_url[-1] == '/':
            print("200 Sent!")
            self.send_200_loc(req_url,dirs)
        elif req_url in dirs:
            print("200 Sent!")
            self.send_200_file(req_url,dirs)
        else:
            print("404 Sent!")
            self.send_404()
        #print(fxn)
        #print('*******************************************')

    def send_200_loc(self,req,dirs):
        length = 0
        reqs = []
        reqs = [x for x in dirs if req in x]
        reqs = [x for x in reqs if (x.count('/')==req.count('/') or (x.count('/')==(req.count('/')+1) and x[-1] == '/'))]
        reqs_link = [x[3:] for x in reqs if x != req and x[0] != '.']
        reqs_show = [x[len(req)-1:] for x in reqs if x != req and x[0] != '.']
        #print(reqs)
        payload = '''
<!DOCTYPE html>
<html>
<body>
	<div class="eg">
		<ul>'''
        for i in range(len(reqs_link)):
            payload += '''
                        <li><a href="'''+reqs_link[i]+'''">'''+reqs_show[i]+'''</a></li>'''
        payload += '''
		</ul>
	</div>
</body>
</html> 
'''
        length = len(payload)
        
        
        response = 'HTTP/1.1 200 OK\r\nContent-type:text/html\r\nContent-length:'+str(length)+'\r\nConnection: close\r\n\r\n'
        if length != 0:
            response = response + payload + '\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))

    def send_200_file(self,req,dirs):
        length = 0
        type_file = 'text/html'
        if 'css' in req:
            type_file = 'text/css'
        with open(req, 'r') as file:
            payload = file.read()
        length = len(payload)
        response = 'HTTP/1.1 200 OK\r\nContent-type:'+type_file+'\r\nContent-length:'+str(length)+'\r\nConnection: close\r\n\r\n'
        if length != 0:
            response = response + payload + '\r\n\r\n'        
        self.request.sendall(bytearray(response,'utf-8'))


    def send_404(self):
        response = 'HTTP/1.1 404 Not Found\r\nContent-type:text/html\r\nContent-length:0\r\nConnection: close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))
        
    def send_405(self):
        response = 'HTTP/1.1 405 Method Not Allowed\r\nContent-type:text/html\r\nContent-length:0\r\nConnection: close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))

    def send_301(self,req):
        new = req[3:]+'/'
        response = 'HTTP/1.1 301 Moved Permanently\r\nLocation:http://127.0.0.1:8080'+new+'\r\nContent-type:text/html\r\nContent-length:0\r\nConnection:close\r\n\r\n'
        self.request.sendall(bytearray(response,'utf-8'))
    

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
