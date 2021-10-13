from threading import Thread

# util 
from util.packetParser import loadsPacket, extractContentsToDict
from util.auth import loginHandler

# exceptions
from exceptions.AuthExceptions import UserNotFoundException
from exceptions.InputExceptions import InvalidInputException

from storage import online_users, all_users, userInList
from User import User

class ClientThread(Thread):
  
  def __init__(self, clientAddress, clientSocket):
    # super()
    Thread.__init__(self)
    self.clientAddress = clientAddress
    self.clientSocket = clientSocket
    self.clientActive = False

    print('=== New connection for: ', clientAddress)
    self.clientActive = True
  
  def run(self):
    message = ''

    while self.clientActive:
      data = self.clientSocket.recv(1024)
      message = data.decode()

      # print(f"message: {message}")

      '''
      if message from client is empty
      client is offline
      '''
      if message == '':
        self.clientActive = False
        print("===== the user disconnected - ", self.clientAddress)
        break

      '''
      parses the message to a readable format
      and handle the different commands
      '''
      (code, contents) = loadsPacket(message)

      if code == "login":
        contents = extractContentsToDict(contents)
        logged = loginHandler(contents, self.clientSocket)

        # since logged in, that means username and password is provided correctly
        if logged:
          self.upgradeConnection(contents)


      if code == "whoelse":
        self.clientSocket.sendall("WHOAMI".encode())
  
  def upgradeConnection(self, contents: dict):
    username, password = contents['user'], contents['password']
    creds = (username, password)

    exists = userInList(creds, all_users)
    if(exists):
      #TODO get used in all list and add to online users
      pass
    
    else:
      new_user = User(username, password)

      # assign user to this thread, to use for method forwarding
      self.user = new_user
      print(all_users)
      all_users.append(self)
      print(all_users[0].user.getUsername())






        



    


