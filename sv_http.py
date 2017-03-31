#coding: utf-8

from sys import argv 

import  webbrowser
import socket
from Shark import Shark

ip = '127.0.0.1'
porta = 8082
diretorio = '/'

if len(argv) >= 4:
	ip = argv[1]
	porta = int(argv[2])
	dir = argv[3]
else:
	print 'Argumentos não encontrados. Executando Padrão'
	
sk = Shark(ip, porta, diretorio)

sk.start()

webbrowser.open(str(ip + ':' + porta))