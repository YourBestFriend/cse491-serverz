# partially from http://docs.python.org/2/library/wsgiref.html

import cgi
import urlparse
import jinja2
from wsgiref.util import setup_testing_defaults

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    	fileSystemLoader = jinja2.FileSystemLoader('./templates')
    	environment = jinja2.Environment(loader=fileSystemLoader)

	getPost = environ['REQUEST_METHOD']
	path = environ['PATH_INFO']
	status = '404 Not Found'
	reply = generateNotFound(environ, environment)
	headers = [('Content-type', 'text/html')]


	if getPost == 'POST':
		if path == '/':
			status = '200 OK'
			reply = generatePost(environ, environment)

		elif path == '/submit':
			status = '200 OK'
			reply = generatePostSubmit(environ, environment)

		else:
			status = '404 Not Found'
			reply = generateNotFound(environ, environment)

	elif getPost == 'GET':
		if path == '/':
			status = '200 OK'
			reply = generateGet(environ, environment)

		elif path == '/content':
			status = '200 OK'
			reply = generateGetContent(environ, environment)

		elif path == '/file':
			status = '200 OK'
			headers = [('Content-type', 'text/plain')]
			reply = generateGetFile(environ, environment)

		elif path == '/image':
			status = '200 OK'
			headers = [('Content-type', 'image/jpeg')]
			reply = generateGetImage(environ, environment)

		elif path == '/submit':
			status = '200 OK'
			reply = generateGetSubmit(environ, environment)

		else:
			status = '404 Not Found'
			generateNotFound(environ, environment)

	else:
		status = '404 Not Found'
		generateNotFound(environ, environment)


	start_response(status, headers)
	#here an array with a single entry is returned to appease validator()
	#response = []
	#response.append(reply)
	#return response

	#but I'm doing this because that array structure no worky with /file or /image... x'(
	return reply
	




	

def generatePost(environ, environment):
	return str(environment.get_template("post.html").render())

def generatePostSubmit(environ, environment):
	headers = {}
	for k in environ.keys():
		headers[k.lower()] = environ[k]	
	FS = cgi.FieldStorage(headers = headers, \
			      fp = environ['wsgi.input'], \
			      environ = environ)
	firstName = FS['firstnamePOST'].value
	lastName = FS['lastnamePOST'].value
	data = {'firstName': firstName, 'lastName': lastName}
	return str(environment.get_template("postSubmit.html").render(data))

def generateGet(environ, environment):
	return str(environment.get_template("get.html").render())

def generateGetContent(environ, environment):
	return str(environment.get_template("getContent.html").render())

def generateGetFile(environ, environment):
	text_file = './files/piracy.txt'
	fp = open(text_file, 'r')
    	data = [fp.read()]
    	fp.close
    	return data

def generateGetImage(environ, environment):
	image_file = './images/Jellyfish.jpeg'
	fp = open(image_file, 'r')
    	data = [fp.read()]
    	fp.close
    	return data

def generateGetSubmit(environ, environment):
	parsedPath = urlparse.parse_qs(environ['QUERY_STRING']);
	firstName = parsedPath['firstnameGET'][0]
	lastName = parsedPath['lastnameGET'][0]
	data = {'firstName': firstName, 'lastName': lastName}
	return str(environment.get_template("getSubmit.html").render(data))

def generateNotFound(environ, environment):
	return str(environment.get_template("notFound.html").render())

def make_app():
	return simple_app
