"""
    Python 3
    Usage: python3 client.py localhost 8080
    coding: utf-8
"""

from socket import *
import sys
import json

# utils
from util.packetParser import dumpsPacket, loadsPacket

if len(sys.argv) != 3:
  print("\n===== Error usage, python3 client.py SERVER_IP SERVER_PORT ======\n")
  exit(0)

'''
config and ports
'''

serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_STREAM)

# build connection with the server and send message to it
clientSocket.connect(serverAddress)

if __name__ == '__main__':

  '''
    authenticate
  '''

  username = input("Username: ")
  parsed = dumpsPacket('login', json.dumps({'user':username})).encode('utf-8')
  clientSocket.sendall(parsed)
  
  authenticated: bool = False
  # wait to recieve
  response = clientSocket.recv(1024)
  data = response.decode()
  code, contents = loadsPacket(data)
  if(code == "200"):
    password = input("Password: ")
    parsed = dumpsPacket('login', json.dumps({'user': username, 'password': password})).encode('utf-8')
    clientSocket.sendall(parsed)

    response = clientSocket.recv(1024)
    data = response.decode()
    code, contents = loadsPacket(data)
    if(code == "200"):
      authenticated = True

  '''
  this loop only starts running
  when the client is authenticated
  '''
  while authenticated:
    message = input()
    if message == 'whoelse':
      parsed = dumpsPacket('whoelse', json.dumps({}))
      # print(parsed)
      clientSocket.sendall(parsed.encode())

      response = clientSocket.recv(1024)
      data = response.decode()
      print(data)


clientSocket.close()