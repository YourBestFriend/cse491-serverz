import server


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
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'GET Name Submission' in conn.sent and \
	   'POST Name Submission' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test GET /content call.
def test_generateGetContent():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'Content ^_^' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test GET /file call.
def test_generateGetFile():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'File ^_^' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test GET /image call.
def test_generateGetImage():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'Image ^_^' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test GET /submit call.
def test_generateGetSubmit():
    conn = FakeConnection("GET /submit?firstname=Bill&lastname=Nye HTTP/1.0HTTP/1.1\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'GET Submit' in conn.sent and \
	   'Howdy thar Mr. Bill Nye!' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test POST / call.
def test_generatePost():
    conn = FakeConnection("POST / HTTP/1.0\r\n" +\
			  "Content-Length: 0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'Howdy World ^_^' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test POST /submit call.
def test_generatePostSubmit():
    conn = FakeConnection("POST /submit HTTP/1.1\r\n" +\
			  "Content-Length: 31\r\n\r\n" +\
			  "firstname=Heyro&lastname=Duncan")
    server.handle_connection(conn)

    assert 'HTTP/1.0 200' in conn.sent and \
	   'POST Submit' in conn.sent and \
	   'Howdy thar Mr. Heyro Duncan!' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test Post Not Found.
def test_PostgenerateNotFound():
    conn = FakeConnection("POST /applesauce HTTP/1.0\r\n" +\
			  "Content-Length: 0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 404 Not Found' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



# Test Get Not Found.
def test_GetgenerateNotFound():
    conn = FakeConnection("GET /applesauce HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)

    assert 'HTTP/1.0 404 Not Found' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)



