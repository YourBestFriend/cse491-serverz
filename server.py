#!/usr/bin/env python
import random
import socket
import time

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
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send("HTTP/1.0 200 OK\r\n")
    c.send("Content-type: text/html\r\n\r\n")
    c.send('''
	<html style='background-color: black;'>

		<body style='border: 5px solid brown; 
				border-radius: 500px; 
				background-color: tan; 
				font-style: italic; 
				padding: 50px; 
				display: inline-block; 
				position: absolute; 
				left: 25%; 
				top: 25%;'>

		  	<h1 id='header' style='color: black; opacity: .5;'>Howdy World ^_^</h1>

		 	<p style='color: dimgray;'>This here is YourBestFriend's Web server!!!</p>

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
	</html>
	''')
    c.close()
