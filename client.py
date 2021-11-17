"""
    Python 3
    Usage: python3 client.py localhost 8080
    coding: utf-8
"""

from socket import *
import sys
import json
import select

# utils
from util.packetParser import dumpsPacket, loadsPacket, extractContentsToDict
from util.Request import post, sendAndWait


# Client Imports
from Client.auth import loginHandler, registerHandler
from Client.broadcast import broadcastHandler
from Client.message import messageHandler
from Client.block import blockHandler, unblockHandler
from Client.private import startPrivateHandler, replyYes, replyNo
from Client.P2PThread import P2PThread

# exceptions
from exceptions.AuthExceptions import UserNotFoundException

if __name__ == '__main__':

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

  open_sockets = []
  open_sockets.append(clientSocket)


  '''
    authenticate
  '''
  authenticated: bool = False
  username = input("Username: ")
  try:
    tries = 1
    while(not authenticated and tries <= 3):
      authenticated = loginHandler(clientSocket, username)
      tries+=1
  except UserNotFoundException as e:
    authenticated = registerHandler(clientSocket, username)

  '''
    this loop only starts running
    when the client is authenticated
  '''

  if authenticated:
    print("Welcome to the greatest messaging application ever!")
  else:
    exit(0)

  
  while authenticated:
    '''
    event loop
    '''
    readers_list = []
    readers_list.append(sys.stdin)
    readers_list += open_sockets
    # this line is super important
    # non blocking i/o
    readers, _, _ = select.select(readers_list, [], [])

    for reader in readers:

      '''
        if connection
      '''
      if reader in open_sockets:
        # if response
        response = clientSocket.recv(1048)
        if(response != "" and response != None):

          code, content = loadsPacket(response.decode())

          if(code == "200" or code == "500" or code=="400"):
            '''
              expects [200] _string
            '''
            print(content, end="")
          
          elif(code == "FIN"):
            print(content)
            clientSocket.close()
            exit(0)
          
          elif(code == "P2P"):
            '''
              expects [200] {'message': _message}
            '''
            print(extractContentsToDict(content)['message'])
          
          elif(code == "P2PCONN"):
            contents = extractContentsToDict(content)
            newP2PSock = socket(AF_INET, SOCK_STREAM)
            address = (contents['ip'], contents['port'])
            
            open_sockets.append(newP2PSock)

            newP2PSock.connect(address)
            print('new socket')
            
            newP2PSock.sendall('hi'.encode())

      else:
        '''
          if user input
        '''
        message = input()
        if message == 'whoelse':
          '''
            Sends this:
            [whoelse] {}
          '''
          post(clientSocket, 'whoelse', {})

        elif message.startswith('whoelsesince'):
          '''
            whoelse since
          '''
          t = ''.join(message.split(" ")[1:])
          post(clientSocket, 'whoelsesince', {'time': t})

        elif message.startswith('broadcast'):
          '''
            broadcast message
          '''
          broadcastHandler(clientSocket, message)
        elif message.startswith('message'):
          '''
            send message
          '''
          messageHandler(clientSocket, message)
        
        elif message.startswith('block'):
          blockHandler(clientSocket, message)
        
        elif message.startswith('unblock'):
          unblockHandler(clientSocket, message)

        elif message.startswith('startprivate'):
          startPrivateHandler(clientSocket, message)

        elif message == 'y' or message == "Y":
          print("BEFO")
          sokt = replyYes(clientSocket)
          open_sockets.append(sokt)

          #starts listening
          sokt.listen()
          print("YES")


        elif message == "n" or message == "N":
          replyNo(clientSocket)


        else:
          print("Error invalid command")
        



# close all connections
for openSocket in open_sockets:
  openSocket.close()