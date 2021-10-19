import socket
import json
from .packetParser import dumpsPacket

'''
Request abstraction functions
abstracts away the socket stuff
'''

def sendAndWait(socket, route, data):
  '''
  sends request
  waits for response 
  then returns response object
  '''
  parsedRequest = dumpsPacket(route, json.dumps(data)).encode('utf-8')
  
  # send socket
  socket.sendall(parsedRequest)

  # waiting for response
  response = socket.recv(1024)

  return response.decode()


