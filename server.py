#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import StringIO
from app import make_app


def main():
	s = socket.socket()         # Create a socket object
	host = socket.getfqdn()     # Get local machine name
	port = random.randint(8000, 9999)
	s.bind((host, port))        # Bind to the port

	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)

	s.listen(5)                 # Now wait for client connection.

	print 'Entering infinite loop; hit CTRL-C to exit'
	while True:
	    # Establish connection with client.    
	    c, (client_host, client_port) = s.accept()
	    handle_connection(c)



def handle_connection(conn):
	#This header gathering idea was taken from:
	#https://github.com/cameronkeif/cse491-serverz/blob/hw4/server.py
	#Before using this code any additional calls to conn.recv() would 
	#cause the server to hang.
	#----------------------------------------------------------------
	requestData = conn.recv(1)

  	# This will get all the headers
  	while requestData[-4:] != '\r\n\r\n':
    		requestData += conn.recv(1)
	#----------------------------------------------------------------

    	
   	#print 'Got connection from', client_host, client_port  <<<<NO WORKY!!!
    	print requestData

	firstLine = requestData.split('\r\n')[0].split(' ')

	getPost = firstLine[0]
	parsedPath = urlparse.urlparse(firstLine[1])
	path = parsedPath[2]

	#setup environ
	environ = {}
	environ['REQUEST_METHOD'] = getPost
	environ['PATH_INFO'] = path




	def start_response(status, response_headers):
		conn.send('HTTP/1.0 ' + status + '\r\n')
		for entry in response_headers:
			key, value = entry
			conn.send(key + ': ' + value + '\r\n')
		conn.send('\r\n')

	if environ['REQUEST_METHOD'] == 'POST':
		#fill the environ(env) dictionary--------
		requestList = requestData.split('\r\n')

		i=1
		while ":" in requestList[i]:
			requestLine = requestList[i].split(": ")			
			environ[requestLine[0].upper()] = requestLine[1]
			i += 1
		#---------------------------------------
	

		#get postContent------------------------
		contentLength = int(environ['CONTENT-LENGTH'])
		postContent = conn.recv(contentLength)
		#---------------------------------------

		environ['wsgi.input'] = StringIO.StringIO(postContent)


	elif environ['REQUEST_METHOD'] == 'GET':
		environ['QUERY_STRING'] = parsedPath.query
	wsgi_app = make_app()
	conn.send(wsgi_app(environ, start_response))
	conn.close()
    	
	

if __name__ == '__main__':
   main()
