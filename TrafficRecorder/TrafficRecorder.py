import sys
import os
import time

class TrafficRecorder(object):
	def __init__(self, application):
		self.application = application

	def __call__(self, environ, start_response):
		f = open('playback.txt', 'a')
		f.write("[ %s ] Request Method: %s, Path Information: %s\n\n" % (time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()), environ['REQUEST_METHOD'], environ['PATH_INFO']))
		f.close()

		response = self.application(environ, start_response)
		response = "".join(response)
		return [response]
