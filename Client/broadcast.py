from util.Request import post
from util.packetParser import loadsPacket

def broadcastHandler(clientSocket, command: str):
  # TODO raise exceptions
  command = command.split(" ")
  #extracts message from [broadcast {message}]
  message = " ".join(command[1:])
  
  post(clientSocket, 'broadcast', {'message': message})