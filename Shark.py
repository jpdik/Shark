#coding: utf-8

import socket
import os
import datetime
import time
import re
import sys
import threading
from time import sleep

SERVER = 'SHARK/1.0'

NOT_FOUND = 'error/404.html'

EXT_PADRAO = 'text/html'

STATUS = {200: "200 OK",
		 404: "404 NOT FOUND"}

RAIZ = '/'

ext = {'html': 'text/html',
	   'htm': 'text/html',
	   'txt': 'plane/txt',
	   'png': 'image/png',
	   'iso': 'application/octetstream'}

class Shark(object):
	def __init__(self, ip, porta, raiz=RAIZ):
		self.nome = SERVER
		self.error = NOT_FOUND
		self.raiz = RAIZ
		self.set_raiz(raiz)

		self.ip = ip
		self.porta = porta
		

	def nome_servidor(self, nome):
		self.nome = nome

	def pagina_erro(self, local):
		self.error = local

	def set_raiz(self, raiz):
		if os.path.exists('./' + raiz):
			if raiz[-1] != '/':
				self.raiz = raiz + '/'
			else:
				self.raiz = raiz
		else:
			print 'diretorio raiz não existente. utilizando raiz (\''+self.raiz+'\')'

	def get_status(self, code):
		return "HTTP/1.1 " + STATUS[code]

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
				diretorio = self.raiz
			else:
				if arq != self.raiz:
					diretorio = self.raiz + arq

			if arq == '':
				arq = 'index.html'

			print diretorio
			f = open('.' + diretorio, 'r')
			dados = f.read()

			utc_datetime = datetime.datetime.utcnow()
			datenow = utc_datetime.strftime("%Y %m %d %H:%M:%S GMT")
			lastmodify = time.ctime(os.path.getmtime(arq))

			content = self.obter_tipo(arq.split('.')[-1].lower())
			

			head = '''{5}
Server: {3}
Date: {1}
Content-Type: {2}
Last-Modified: {4}
Content-Length: {0}

'''.format(len(dados), datenow, content, self.nome, lastmodify, self.get_status(200))
		
		except IOError as e:

			info = self.gerar_lista_index(diretorio)
			if len(info) > 0:
				head = info[0]
				dados = info[1]
			
			else:
				head = '''{0}

'''.format(self.get_status(404))

				dados = open(self.error, 'r').read()

		except IndexError:
			head = '''{0}

'''.format(self.get_status(404))

			dados = open(self.error, 'r').read()

		return head + dados



	def gerar_lista_index(self, dir):
		if os.path.exists('.' + dir):
			files = os.listdir('.' + dir)
			dir = dir[dir.find('/'):]
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
				dados += '<dt><a href="..">..</dt>'
				dados += '<dt><a href=".">.</dt>'
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

	def requisicao_cliente(self, con, info_cli):
		req = con.recv(1024)

		page = self.obter_pagina(req)

		#print page
		con.send(page)

		con.close()

	def start(self):
		#try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		s.bind((self.ip, self.porta))

		print self.ip

		s.listen(5)

		print 'Servidor Shark Escutando. IP: {0}, Porta: {1}'.format(self.ip, self.porta)

		while True:
			try:
				con, info_cli = s.accept()
				t1 = threading.Thread(target=self.requisicao_cliente, args=[con, info_cli])
				t1.start()
			except KeyboardInterrupt:
				print 'Finalizando host...'
				sys.exit(0)

	