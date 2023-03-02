# test a Python client calling our cherrypy server main.py
# command shell commands:
    # arp -a         # inspect LAN - local area network
    # ipconfig       # summary of this computer's IP environment
# IP addresses that may be useful:
    # 192.168.0.1    # router for LAN (password needed)

    
from pprint import pprint
import http.client

conn = http.client.HTTPConnection('127.0.0.1', 8080, timeout=100)
print(conn)

def request_wait_print(mode, url):
    global conn
    conn.request(mode, url)
    response = conn.getresponse().read()
    print(response)

if True:  
    request_wait_print('GET', '/')
    request_wait_print('GET', '/changeParagraph')
    request_wait_print('GET', '/changeParagraph?text=This+text%20should+echo')
    request_wait_print('PUT', '/changeParagraph?text=This+and+that%%')
    request_wait_print('GET', '/changeParagraph?text=array')
    request_wait_print('GET', '/greetUser')
    request_wait_print('GET', '/greetUser?name=Jojo')

