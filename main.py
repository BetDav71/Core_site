import socket
from urlpattern import urlpattern
from views import *
from cookies import *


class Server():
	def __init__(self,host,ip):
		self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.HOST = host
		self.PORT = ip
		self.server_socket.bind((self.HOST,self.PORT))

	def post_params(self,request):
		# par = request.split('\r\n')[1:-1]
		# d = {}
		# for i in par:
		# 	try:
		# 		a = i.split(':')
		# 		d[a[0].strip()] = a[1].strip()
		# 	except:
		# 		continue
		try:
			parr = request.split('\r\n\r\n')[-1]
			parr1 = parr.split('&')
			d1 = {}
			for i in parr1:
				d1[i.split('=')[0]] = i.split('=')[1]
		except:
			d1 = {}
		return d1


	#GET PARAMETRS of 'GET METHOD'
	def get_params(self,parametrs):
		params = parametrs.split('&')
		d = {}
		for param in params:
			k,w = param.split('=')
			d[k] = w
		return d

	#PARSE URL 
	def clear_url(self,url):
		clear_url = ''
		if '?' not in url:
			clear_url = url
			parametrs = {}
			return (clear_url,parametrs)
		else:
			params = url.split('?')
			clear_url = params[0]
			parametrs1 = params[1]
			parametrs = self.get_params(parametrs1)
			return (clear_url,parametrs)

	#PARSE REQUEST
	def parse_request(self,request):
		parse = request.split(' ')
		try:
			url = parse[1]
			method = parse[0]
			return (method,url)
		except:
			url = ''
			method = ''
			return (method,url)

	#GENERATE HEADERS (code)
	def generate_headers(self,method,url):
		if method != 'GET' and method != 'POST':
			return ('HTTP/1.1 405 Method not allowed',405)
		if not url in urlpattern:
			return ('HTTP/1.1 404 Page not found',404)

		return ('HTTP/1.1 200 OK',200)


	#GENERATE HTML (CONTENT)
	def generate_content(self,code,url,get_params,post_params):
		if code == 404:
			return '<h1>404 Page not found</h1>'
		if code == 405:
			return '<h1>405 Method not allowed</h1>'
		return urlpattern[url](get_params,post_params)

	def set_cookies(self,parametres_for_cookies):
		string = ''
		for param in parametres_for_cookies:
			string += '\r\nSet-Cookie: %s=%s' % (param,parametres_for_cookies[param])
		return string

	# GENERAE ANSWER FROM SERVER (RESPONSE)
	def generate_response(self,request):
		method,url = self.parse_request(request)
		clear_url , get_params = self.clear_url(url)
		post_params = self.post_params(request)
		headers , code = self.generate_headers(method,clear_url)
		global cookies_params
		cookies_params = cookies_param
		body = self.generate_content(code,clear_url,get_params,post_params)
		cookies = self.set_cookies(cookies_params)
		headers += cookies + '\n\n'
		return (headers + body).encode()




	def run(self):
		self.server_socket.listen(10)
		while True:
			client_sock,addr = self.server_socket.accept()
			request = client_sock.recv(1024)	
			print(request.decode('utf-8'))
			response = self.generate_response(request.decode('utf-8'))
			client_sock.sendall(response)
			client_sock.close()



server = Server('localhost',8080)
server.run()