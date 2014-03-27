#!/usr/bin/env python
import random
import socket
import time
import urlparse
import StringIO
from app import make_app
from wsgiref.validate import validator
import sys
import argparse
import quixote
import imageapp
import quotes
import chat




def main():
	parser = argparse.ArgumentParser(description='Servers applications')
	parser.add_argument('-p', metavar='-p', type=int, nargs='?', default=-1, help='the port number')
	parser.add_argument('-A', metavar='-A', type=str, nargs=1, help='the app to run (image, altdemo, or myapp)')

	desiredApp = parser.parse_args().A[0]
	desiredPort = parser.parse_args().p

	supportedApps = ['myapp', 'image', 'altdemo', 'quotes', 'chat']

	if desiredApp not in supportedApps:
		print "I'm afraid this app is not currently supported"
	   	sys.exit()


	s = socket.socket()         # Create a socket object
	host = socket.getfqdn()     # Get local machine name

	port = desiredPort
	if port < 8000 or port > 9999:
      		port = random.randint(8000,9999)

	s.bind((host, port))        # Bind to the port


	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)

	s.listen(5)                 # Now wait for client connection.

	print 'Entering infinite loop; hit CTRL-C to exit'
	while True:
	    # Establish connection with client.    
	    c, (client_host, client_port) = s.accept()
	    handle_connection(c, host, port, desiredApp)



def handle_connection(conn, host, port, desiredApp):
	environ = {}

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

	#create environ entries
	environ['REQUEST_METHOD'] = getPost
	environ['PATH_INFO'] = path
	environ['SCRIPT_NAME'] = '' #this is required for quixote demo app to work!




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

		environ['HTTP_COOKIE'] = environ['COOKIE'] if environ.get('COOKIE') else ''
		environ['wsgi.input'] = StringIO.StringIO(postContent)
		environ['QUERY_STRING'] = ''

		#required for validator to not complain
		environ['SERVER_NAME'] = host
		environ['SERVER_PORT'] = str(port)
		environ['wsgi.version'] = (1, 0)
		environ['wsgi.errors'] = sys.stderr
		environ['wsgi.multithread'] = False
        	environ['wsgi.multiprocess'] = False
        	environ['wsgi.run_once'] = False
        	environ['wsgi.url_scheme'] = "http"


	elif environ['REQUEST_METHOD'] == 'GET':
		environ['HTTP_COOKIE'] = ''
		environ['wsgi.input'] = StringIO.StringIO('')
		environ['QUERY_STRING'] = parsedPath.query

		#required for validator to not complain
		environ['SERVER_NAME'] = 'localhost'
		environ['SERVER_PORT'] = str(port)
		environ['wsgi.version'] = (1, 0)
		environ['wsgi.errors'] = sys.stderr
		environ['wsgi.multithread'] = False
        	environ['wsgi.multiprocess'] = False
        	environ['wsgi.run_once'] = False
        	environ['wsgi.url_scheme'] = "http"



	#serve the desired application
	if desiredApp == 'myapp':    #validator is disabled because it no worky with /file or /image... x'(
		new_app = make_app()#validator(make_app())

    	elif desiredApp == 'image':
        	imageapp.setup()
    		p = imageapp.create_publisher()
		new_app = quixote.get_wsgi_app()

	elif desiredApp == 'altdemo':
		#from quixote.demo import create_publisher
	    	#from quixote.demo.mini_demo import create_publisher
		from quixote.demo.altdemo import create_publisher
		p = create_publisher()
		new_app = quixote.get_wsgi_app()

	elif desiredApp == 'quotes':
		directory_path = './quotes/'
    		new_app = quotes.create_quotes_app(directory_path + 'quotes.txt', directory_path + 'html')

	elif desiredApp == 'chat':
		new_app = chat.create_chat_app('./chat/html')

		
	result = new_app(environ, start_response)
	for item in result:
		conn.send(item)
	conn.close()
    	
	

if __name__ == '__main__':
   main()
