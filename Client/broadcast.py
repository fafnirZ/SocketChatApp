from util.Request import sendAndWait
from util.packetParser import loadsPacket

def broadcastHandler(clientSocket, command: str):
  command = command.split(" ")
  #extracts message from [broadcast {message}]
  message = " ".join(command[1:])
  
  response = sendAndWait(clientSocket, 'broadcast', {'message': message})
  code, contents = loadsPacket(response)