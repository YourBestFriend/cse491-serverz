import server

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

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True



# Test GET / call.
def test_generateGet():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>ZZZzzzz -_-</h1>" + \
		      "<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/content'>Content</a>" + \
		      "<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/file'>File</a>" + \
		      "<a style='color: DarkSlateGray; margin: 15px; text-decoration: none;' href='/image'>Image</a>" + \
		      "<p>GET Name Submission</p><form action='/submit' method='GET'><input style='width: 150px' type='text' name='firstname'><input style='width: 150px' type='text' name='lastname'><input type='submit' value='Submit'></form>" + \
		      "<p>POST Name Submission</p><form action='/submit' method='POST'><input style='width: 150px'type='text' name='firstname'><input style='width: 150px' type='text' name='lastname'><input type='submit' value='Submit'></form>" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test GET /content call.
def test_generateGetContent():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>Content ^_^</h1>" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test GET /file call.
def test_generateGetFile():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>File ^_^</h1>" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test GET /image call.
def test_generateGetImage():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>Image ^_^</h1>" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test GET /submit call.
def test_generateGetSubmit():
    conn = FakeConnection("GET /submit?firstname=Bill&lastname=Nye HTTP/1.0HTTP/1.1\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>GET Submit</h1>" + \
		      "Howdy thar Mr. Bill Nye!" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test POST / call.
def test_generatePost():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>Howdy World ^_^</h1>" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)



# Test POST /submit call.
def test_generatePostSubmit():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n\r\nfirstname=Bill&lastname=Nye")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
		      "Content-type: text/html\r\n\r\n" + \
		      content1 + \
	              "<h1 id='header' style='color: black; opacity: .5;'>POST Submit</h1>" + \
		      "Howdy thar Mr. Bill Nye!" + \
		      content2

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

