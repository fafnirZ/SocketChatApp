'''
functions for authentications and authorisation
to be forwarded to ClientThread
'''
import os

# utils
from util.packetParser import dumpsPacket

# exceptions
from exceptions.AuthExceptions import UserNotFoundException, InvalidCredentialsException
from exceptions.InputExceptions import InvalidInputException

# imports
from Server.credentials import saveCredentials, getAllCredentials

'''
checks if the username provided is in credenitals file
'''
def checkUsername(username: str) -> bool:
  credentials = getAllCredentials()
  
  for l in credentials:
    user, _ = l.split(" ")
    if user == username:
      return True
  return False
  
'''
checks if username and password is the same as 
the one stored in credentials file
'''
def checkCredentials(username:str, password:str) -> bool:
  credentials = getAllCredentials()
  for l in credentials:
    user, pwd = l.split(" ")
    # print(password)
    if user == username and pwd == password:
      return True

  return False

'''
handler for login function
'''
def loginHandler(contents:dict, socket) -> bool:
  # print(contents)
  try:
    if(len(contents) < 1 or len(contents) > 2):
      raise InvalidInputException

    if(len(contents) == 2):
      '''
      this is the only branch which should return true
      checks credentials and sends response back to user
      '''
      if(checkCredentials(contents['user'], contents['password'])):
        response = dumpsPacket(200, "success").encode('utf-8')
        socket.sendall(response)
        return True
      else:
        raise InvalidCredentialsException

    elif (len(contents) == 1):
      if checkUsername(contents['user']):
        # ask for password
        # send a response to front end saying to check for credentials
        response = dumpsPacket(200, "success").encode('utf-8')
        socket.sendall(response)
      else:
        raise UserNotFoundException
  
  except InvalidCredentialsException as e:
    # todo handle exceptions and send back to client
    response = dumpsPacket(401, "Invalid Credentials").encode('utf-8')
    socket.sendall(response)
    return

  except UserNotFoundException as e:
    # print('user is not found')
    response = dumpsPacket(400, "User not found").encode('utf-8')
    socket.sendall(response)
    return

  except InvalidInputException as e:
    print('input is invalid')
    return
  
  return False


'''
  register handler
'''
def registerHandler(contents: dict, socket) -> bool:
  '''
    TODO checks
    assumptions: just append to the end
  '''
  saveCredentials(contents['user'], contents['password'])

