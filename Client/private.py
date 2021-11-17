from util.Request import post
from util.packetParser import dumpsPacket
from socket import *

def startPrivateHandler(socket, command:str):
  '''
    command: startprivate _user
    format:
    {
      'target' : _user
    }
    packet format:
    [message] {'target': _user}

    response format:
    [200] ""

    error format:
    [400] user has declined
    [400] the user has blocked you
    [400] a private connection with user is already established
  '''
  command = command.split(" ")
  target = command[1]

  post(socket, 'startprivate', {'target': target})
  

def replyYes(EstablisherSocket):
  '''
    create new socket and send 
  '''
  sock = socket(AF_INET, SOCK_STREAM)
  sock.bind(('', 0))
  sock.listen()

  # send sock information to other client via server
  post(EstablisherSocket, 200, {'ip': sock.getsockname()[0], 'port': sock.getsockname()[1]})

  # wait till connection is established
  sockt, addr = sock.accept()
  return sockt

def replyNo(socket):
  post(socket, 400, {'reply': "no"})



def privateMessageHandler(open_sockets, username: str, command: str):

  command = command.split(" ")
  target = command[1]
  message = " ".join(command[2:])

  peerSocket = None
  for sokt in open_sockets:
    if sokt['connection'] == target:
      peerSocket= sokt['socket']
  
  if(peerSocket != None):
    # send messages
    peerSocket.sendall(dumpsPacket(200, f"{username} (private): {message}\n").encode())


def stopPrivateHandler(open_sockets, username: str, command: str):

  command = command.split(" ")
  target = command[1]

  for i, sock in enumerate(open_sockets):
    if sock['connection'] == target:
      sockt = open_sockets.pop(i)
      sockt['socket'].sendall(dumpsPacket(200, f"{username} has closed your private connection\n").encode())
      sockt['socket'].close()