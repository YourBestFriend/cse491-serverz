#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import StringIO
import jinja2


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
	fileSystemLoader = jinja2.FileSystemLoader('./templates')
	environment = jinja2.Environment(loader=fileSystemLoader)

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




    	if getPost == 'POST':
		#fill the postHeaders dictionary--------
		postHeaders = {}

		requestList = requestData.split('\r\n')

		i=1
		while ":" in requestList[i]:
			requestLine = requestList[i].split(": ")			
			postHeaders[requestLine[0]] = requestLine[1]
			i += 1
		#---------------------------------------
		

		#get postContent------------------------
		contentLength = int(postHeaders['Content-Length'])
		postContent = conn.recv(contentLength)
		#---------------------------------------

		
		FS = cgi.FieldStorage(headers = postHeaders, \
				      fp = StringIO.StringIO(postContent), \
				      environ = {'REQUEST_METHOD': 'POST'})


		if path == '/':
			generatePost(conn, environment)

		elif path == '/submit':
			generatePostSubmit(conn, environment, FS)

		else:
			generateNotFound(conn, environment)

	elif getPost == 'GET':
		if path == '/':
			generateGet(conn, environment)

		elif path == '/content':
			generateGetContent(conn, environment)

		elif path == '/file':
			generateGetFile(conn, environment)

		elif path == '/image':
			generateGetImage(conn, environment)

		elif path == '/submit':
			generateGetSubmit(conn, environment, parsedPath[4])

		else:
			generateNotFound(conn, environment)





		

def generatePost(conn, environment):
	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("post.html").render()
	conn.send(reply)
	conn.close()

def generatePostSubmit(conn, environment, FS):	
	firstName = FS['firstname'].value
	lastName = FS['lastname'].value
	
	data = {'firstName': firstName, 'lastName': lastName}

	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("postSubmit.html").render(data)
	conn.send(reply)
	conn.close()

def generateGet(conn, environment):
	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("get.html").render()
	conn.send(reply)
	conn.close()

def generateGetContent(conn, environment):
	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("getContent.html").render()
	conn.send(reply)
	conn.close()

def generateGetFile(conn, environment):
	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("getFile.html").render()
	conn.send(reply)
	conn.close()

def generateGetImage(conn, environment):
	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("getImage.html").render()
	conn.send(reply)
	conn.close()

def generateGetSubmit(conn, environment, parsedPath):
	parsedPath = urlparse.parse_qs(parsedPath);
	
	firstName = parsedPath['firstname'][0]
	lastName = parsedPath['lastname'][0]
	
	data = {'firstName': firstName, 'lastName': lastName}

	reply = "HTTP/1.0 200 OK\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("getSubmit.html").render(data)
	conn.send(reply)
	conn.close()

def generateNotFound(conn, environment):
	reply = "HTTP/1.0 404 Not Found\r\n" + \
		"Content-type: text/html\r\n\r\n" + \
		environment.get_template("notFound.html").render()
	conn.send(reply)
	conn.close()
	

if __name__ == '__main__':
   main()
