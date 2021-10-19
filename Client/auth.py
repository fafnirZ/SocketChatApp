import json

from exceptions.AuthExceptions import UserNotFoundException
from util.packetParser import dumpsPacket, loadsPacket
from util.Request import sendAndWait
'''
login and register handlers
'''

def loginHandler(clientSocket, username) -> bool:

  authenticated: bool = False
  response = sendAndWait(clientSocket, 'login', {'user':username})
  code, contents = loadsPacket(response)
  if(code == "200"):
    password = input("Password: ")
    response = sendAndWait(clientSocket, 'login', {'user': username, 'password': password})
    code, contents = loadsPacket(response)
    if(code == "200"):
      authenticated = True
    elif(code == "401"):
      # TODO login failed retry
      # raise exception and allow for another try
      print(contents)
  elif(code == "400"):
    # TODO username not found register username
    raise UserNotFoundException
  
  # normally username is not returned
  return authenticated


def registerHandler(clientSocket, username) -> bool:
  authenticated: bool = False
  password = input("This is a new user. Enter a password: ")
  response = sendAndWait(clientSocket, 'register', {'user': username, 'password': password})
  code, contents = loadsPacket(response)

  if(code == "200"):
    authenticated = True
  else:
    #TODO something wrong happened
    pass
  
  return authenticated