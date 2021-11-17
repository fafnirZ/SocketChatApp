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
from Client.private import startPrivateHandler, replyYes, replyNo, privateMessageHandler

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

  '''
    open_sockets is a HM
    'username': socket
  '''
  open_sockets = []
  open_sockets.append({'connection': 'server', 'socket': clientSocket})


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
    
    # map sockets from dictionary to a list
    open_sockets_as_list = list(map(lambda x: x['socket'], open_sockets))
    readers_list += open_sockets_as_list

    # this line is super important
    # non blocking i/o
    readers, _, _ = select.select(readers_list, [], [])

    for reader in readers:

      '''
        if connection
      '''
      if reader in open_sockets_as_list:
        # if response
        response = reader.recv(1048)
        if(response != "" and response != None and len(response) > 0):
          # print(response)
          code, content = loadsPacket(response.decode())

          if(code == "200" or code == "500" or code=="400"):
            '''
              expects [200] _string
            '''
            print(content, end="")
          
          elif(code == "FIN"):
            '''
              to close client
            '''
            print(content)
            for sock in open_sockets:
              sock['socket'].close()
            exit(0)
          
          elif(code == "P2P"):
            '''
              expects [200] {'message': _message}
            '''
            print(extractContentsToDict(content)['message'])
          
          elif(code == "P2PCONN"):
            '''
              initialising client runs this function
            '''
            contents = extractContentsToDict(content)
            newP2PSock = socket(AF_INET, SOCK_STREAM)
            address = (contents['ip'], contents['port'])
            user = contents['username']
            try:
              newP2PSock.connect(address)
              print(f'{user} accepts private messaging')
            except:
              print('connection faileddd')
              pass
            
            # add to open sockets
            open_sockets.append({'connection': user, 'socket' : newP2PSock})

            # send via p2p
            # uses the global username
            newP2PSock.sendall(dumpsPacket("P2PCONNACK", json.dumps({'username': username})).encode())

          elif(code == "P2PCONNACK"):
            '''
              accepting client runs this function
              upgrades socket stored in all_sockets to include
              'connection': _username
            '''
            # need to acknowledge connection open by sending the other
            # client with the username
            contents = extractContentsToDict(content)

            # find the dictionary which matches the current socket
            # updates the hashtable to include username 
            for sock in open_sockets:
              if sock['socket'] == reader:
                sock['connection'] = contents['username']


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
        
        elif message.startswith('private'):
          privateMessageHandler(open_sockets, username, message)



        elif message == 'y' or message == "Y":
          sokt = replyYes(clientSocket)
          open_sockets.append({'socket': sokt})
          #print(readers_list)
          #starts listening

        elif message == "n" or message == "N":
          replyNo(clientSocket)

        else:
          print("Error invalid command")
        



# close all connections
for sock in open_sockets:
  sock['socket'].close()