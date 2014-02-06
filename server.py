#!/usr/bin/env python
import random
import socket
import time
import urlparse

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
	requestData = conn.recv(1000)
    	
   	#print 'Got connection from', client_host, client_port  <<<<NO WORKY!!!
    	print requestData
	
	firstLine = requestData.split('\r\n')[0].split(' ')

	getPost = firstLine[0]
	parsedPath = urlparse.urlparse(firstLine[1])
	path = parsedPath[2]

	

	#=========================== PAGE CONTENT =================================================
	content1 = """<html style='background-color: black;'>

			<body style='border: 5px solid brown; 
					border-radius: 500px; 
					background-color: tan; 
					font-style: italic; 
					padding: 50px; 
					display: inline-block; 
					position: absolute; 
					left: 25%; 
					top: 25%;'>"""

			 #<h1 id='header' style='color: black; opacity: .5;'>Howdy World ^_^</h1>

	content2 = """    <p style='color: dimgray;'>This here is YourBestFriend's Web server!!!</p>

			  <script type='text/javascript'>
				window.setInterval(function(){ changeColor(); }, 75);
				var color = 'red';

				function changeColor()
				{ 
					document.getElementById('header').style.color= color; newColor();
				}

				function newColor()
				{   
					if(color == 'red'){color = 'darkorange';} 
					else if(color == 'darkorange'){color = 'yellow';} 
					else if(color == 'yellow'){color = 'chartreuse';} 
					else if(color == 'chartreuse'){color = 'cyan';} 
					else if(color == 'cyan'){color = 'indigo';} 
					else if(color == 'indigo'){color = 'red';}   
				}
			  </script>

		        </body>
	              </html>"""
	#==========================================================================================


    	if getPost == 'POST':
		if path == '/':
			generatePost(conn, content1, content2)
		elif path == '/submit':
			generatePostSubmit(conn, content1, content2, requestData.split('\r\n')[-1])

	elif getPost == 'GET':
		if path == '/':
			generateGet(conn, content1, content2)

		elif path == '/content':
			generateGetContent(conn, content1, content2)

		elif path == '/file':
			generateGetFile(conn, content1, content2)

		elif path == '/image':
			generateGetImage(conn, content1, content2)

		elif path == '/submit':
			generateGetSubmit(conn, content1, content2, parsedPath[4])
		

def generatePost(conn, content1, content2):
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>Howdy World ^_^</h1>")
	conn.send(content2)
	conn.close()

def generatePostSubmit(conn, content1, content2, parsedPath):
	parsedPath = urlparse.parse_qs(parsedPath);
	
	firstName = parsedPath['firstname'][0]
	lastName = parsedPath['lastname'][0]
	
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>POST Submit</h1>")
	conn.send("Howdy thar Mr. %s %s!" % (firstName, lastName))
	conn.send(content2)
	conn.close()

def generateGet(conn, content1, content2):
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>ZZZzzzz -_-</h1>")
	conn.send("<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/content'>Content</a>")
	conn.send("<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/file'>File</a>")
	conn.send("<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/image'>Image</a>")
	conn.send("<p>GET Name Submission</p><form action='/submit' method='GET'><input style='width: 150px' type='text' name='firstname'><input style='width: 150px' type='text' name='lastname'><input type='submit' value='Submit'></form>")
	conn.send("<p>POST Name Submission</p><form action='/submit' method='POST'><input style='width: 150px'type='text' name='firstname'><input style='width: 150px' type='text' name='lastname'><input type='submit' value='Submit'></form>")
	conn.send(content2)
	conn.close()

def generateGetContent(conn, content1, content2):
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>Content ^_^</h1>")
	conn.send(content2)
	conn.close()

def generateGetFile(conn, content1, content2):
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>File ^_^</h1>")
	conn.send(content2)
	conn.close()

def generateGetImage(conn, content1, content2):
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>Image ^_^</h1>")
	conn.send(content2)
	conn.close()

def generateGetSubmit(conn, content1, content2, parsedPath):
	parsedPath = urlparse.parse_qs(parsedPath);
	
	firstName = parsedPath['firstname'][0]
	lastName = parsedPath['lastname'][0]
	
	conn.send("HTTP/1.0 200 OK\r\n")
    	conn.send("Content-type: text/html\r\n\r\n")
    	conn.send(content1)
	conn.send("<h1 id='header' style='color: black; opacity: .5;'>GET Submit</h1>")
	conn.send("Howdy thar Mr. %s %s!" % (firstName, lastName))
	conn.send(content2)
	conn.close()

	

if __name__ == '__main__':
   main()
