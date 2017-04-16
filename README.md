# Shark
Servidor HTTP Simples

Programado em Socket na linguagem python na Disciplia de Redes do 3º período
do Curso Tecnologia em Sistemas para Internet, com a orietanção do Professor Rafael Alencar.

O servidor criado usará a pasta raiz de onde a aplicação for executada, mas pode ser alterada por parâmetro.

Exemplo de um programa simples em python:

<pre>
#coding: utf-8

import socket
from Shark import Shark

sk = Shark('127.0.0.1', 8082)

sk.start()
</pre>

Onde são passados dois parâmetros para o construdor do HTTP (Shark)
O primeiro é o IP onde será rodado o servidor (IP local ou IP da máquina)
O segundo é a porta onde será executado o servidor.
<pre>
sk = Shark('127.0.0.1', 8082)
</pre>

Passando um terceiro parâmetro para mudar a raiz do servidor.
Exemplo:
<pre>
sk = Shark('127.0.0.1', 8082, '/www')
</pre>

Para iniciar o servidor é chamado a função start() do Shark:
<pre>
sk.start()
</pre>

O programa também pode ser executado atráves de argumentos passados na linha de Comando:
Exemplo:
<pre>
python sv_http.py 127.0.0.1 8082 '/'
  
ou
  
python sv_http.py 127.0.0.1 8082
</pre>
  
Após o servidor estar executando, basta chamar o servidor no Navegador atraves do IP:PORTA:
Exemplo:
<pre>
127.0.0.1:8082
</pre>
