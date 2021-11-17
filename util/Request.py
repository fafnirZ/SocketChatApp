import socket
import json
from .packetParser import dumpsPacket
from .recv import recv_timeout



def sendAndWait(socket, route, data):

  #sends request
  #waits for response 
  #then returns response object

  parsedRequest = dumpsPacket(route, json.dumps(data)).encode('utf-8')
  
  # send socket
  socket.sendall(parsedRequest)

  # waiting for response
  response = socket.recv(1024)


  return response.decode()

def sendAndWaitTimeout2(socket, route, data):

  #sends request
  #waits for response 
  #then returns response object

  parsedRequest = dumpsPacket(route, json.dumps(data)).encode('utf-8')
  
  # send socket
  socket.sendall(parsedRequest)

  # waiting for response
  response = recv_timeout(socket)
  print(response)
  return response


def post(socket, route, data):
  parsedRequest = dumpsPacket(route, json.dumps(data)).encode('utf-8')
  
  # send socket
  socket.sendall(parsedRequest)