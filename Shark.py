#coding: utf-8

import socket
import os
import datetime
import time
import re
import sys

SERVER = 'SHARK/1.0'

NOT_FOUND = 'error/404.html'

EXT_PADRAO = 'text/html'

ext = {'html': 'text/html',
	   'htm': 'text/html',
	   'txt': 'plane/txt',
	   'png': 'image/png'}

class Shark(object):
	def __init__(self, ip, porta, tipo):
		self.nome = SERVER
		self.error = NOT_FOUND

		self.ip = ip
		self.porta = porta
		self.tipo = tipo

	def nome_servidor(self, nome):
		self.nome = nome

	def pagina_erro(self, local):
		self.error = local

	def nome_camada_transporte(self, cod):
		if cod == socket.SOCK_STREAM:
			return 'TCP'
		elif cod == SOCK_DGRAM:
			return 'UDP'
		else:
			return 'UNKNOWN'

	def obter_tipo(self, tipo):
		if tipo not in ext:
			content = EXT_PADRAO
		else:
			content = ext[tipo]

		return content

	def obter_pagina(self, req):
		try:
			tipo = re.findall('(.*?) /', req)[0]
			arq = re.findall('{0} /(.*?) '.format(tipo), req)[0]
			diretorio = re.findall('{0} (.*?) '.format(tipo), req)[0]

			if diretorio == '':
				diretorio = '/'

			if arq == '':
				arq = 'index.html'

			f = open(arq, 'r')
			dados = f.read()

			utc_datetime = datetime.datetime.utcnow()
			datenow = utc_datetime.strftime("%Y %m %d %H:%M:%S GMT")
			lastmodify = time.ctime(os.path.getmtime(arq))

			content = self.obter_tipo(arq.split('.')[-1].lower())
			

			head = '''HTTP/1.1 200 OK
Server: {3}
Date: {1}
Content-Type: {2}
Last-Modified: {4}
Content-Length: {0}

'''.format(len(dados), datenow, content, self.nome, lastmodify)
		
		except IOError as e:

			info = self.gerar_lista_index(diretorio)
			if len(info) > 0:
				head = info[0]
				dados = info[1]
			
			else:
				head = '''HTTP/1.1 404 NOT FOUND

				'''

				dados = open(self.error, 'r').read()

		except IndexError:
			head = '''HTTP/1.1 404 NOT FOUND

				'''

			dados = open(self.error, 'r').read()

		return head + dados



	def gerar_lista_index(self, dir):
		if os.path.exists('.' + dir):
			files = os.listdir('.' + dir)
			dados = '''<html>
<head>
<head>
<body>
<h1>Index of '''
			dados += dir + '</h1><br /><dl>'
			if dir != '/':
				raiz = dir[:dir.rfind('/')]
				if len(raiz) < 1:
					raiz = '/'
				dados += '<dt><a href="/">..</dt>'
				dados += '<dt><a href="'+raiz+'">.</dt>'
				for i in files:
					dados += '<dt><a href="'+dir+'/'+i+'">'+i+'</dt>'					
			else:
				for i in files:
					dados += '<dt><a href="'+i+'">'+i+'</dt>'

			dados+='''</dl></body>
</html>'''

			head = '''HTTP/1.1 200 OK
Server: {1}
Content-Length: {0}

'''.format(len(dados), self.nome)
			return (head, dados)
		else:
			return ()

	def start(self):
		#try:
		s = socket.socket(socket.AF_INET, self.tipo)

		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		s.bind((self.ip, self.porta))

		s.listen(1)

		print 'Servidor {2} Escutando. IP: {0}, Porta: {1}'.format(self.ip, self.porta, self.nome_camada_transporte(self.tipo))

		while True:
			try:
				con, info_cli = s.accept()

				req = con.recv(1024)

				page = self.obter_pagina(req)

				#print page
				con.send(page)
				con.close()
			except KeyboardInterrupt:
				print 'Finalizando host...'
				sys.exit(0)

	