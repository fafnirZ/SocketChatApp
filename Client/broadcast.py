from util.Request import sendAndWait

def broadcastHandler(clientSocket, command: str):
  command = command.split(" ")
  #extracts message from [broadcast {message}]
  message = " ".join(command[1:])
  
  response = sendAndWait(clientSocket, 'broadcast', {'message': message})
  code, contents = loadsPacket(response)
  print(code)
  print(contents)
  if(code == "200"):
    print(contents)