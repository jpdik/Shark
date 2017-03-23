#coding: utf-8

import socket
import os
import datetime
import time
import re

SERVER = 'JP/1.0'

NOT_FOUND = 'error/404.html'

EXT = {'html': 'text/html',
	   'htm': 'text/html',
	   'txt': 'plane/txt',
	   'png': 'image/png'}


def gerar_lista_index():
	files = os.listdir('./')
	dados = '''<html>
<head>
<head>
<body>
	<h1>Index of /</h1'''
	for i in files:
		dados = dados + '<a href="'+i+'">'+i+'<br />'

	dados+='''</body>
</html>
'''

	head = '''HTTP/1.1 200 OK
Server: {1}
Content-Length: {0}

'''.format(len(dados), SERVER)
	return (head, dados)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('127.0.0.1', 8081))

s.listen(1)

while True:

	con, info_cli = s.accept()

	req = con.recv(1024)

	try:
		diretorio = re.findall('GET /(.*?) ', req)[0]

		if diretorio == '':
			diretorio = 'index.html'

		f = open(diretorio, 'r')
		dados = f.read()

		utc_datetime = datetime.datetime.utcnow()
		datenow = utc_datetime.strftime("%Y %m %d %H:%M:%S GMT")
		if diretorio.split('.')[-1].lower() not in EXT:
			content = 'text/html'
		else:
			content = EXT[diretorio.split('.')[-1].lower()]
		lastmodify = time.ctime(os.path.getmtime(diretorio))

		head = '''HTTP/1.1 200 OK
Server: {3}
Date: {1}
Content-Type: {2}
Last-Modified: {4}
Content-Length: {0}

'''.format(len(dados), datenow, content, SERVER, lastmodify)
		
	except IOError:

		if diretorio == 'index.html':
			info = gerar_lista_index()
			head = info[0]
			dados = info[1]
		else:
			head = '''HTTP/1.1 404 NOT FOUND

			'''

			dados = open(NOT_FOUND, 'r').read()
	except IndexError:

		if diretorio == 'index.html':
			info = gerar_lista_index()
			head = info[0]
			dados = info[1]
		else:
			head = '''HTTP/1.1 404 NOT FOUND

			'''

			dados = open(NOT_FOUND, 'r').read()


	page = head + dados

	print page
	con.send(page)
	con.close()