from threading import Thread

# util 
from util.packetParser import loadsPacket, extractContentsToDict
from util.auth import loginHandler
from util.whoelse import whoelse

# exceptions
from exceptions.AuthExceptions import UserNotFoundException
from exceptions.InputExceptions import InvalidInputException

from storage import userOnline, userExists, addOnlineUsers, addAllUsers, setUserOffline
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

        # removes current thread from list of threads in online_users
        setUserOffline(self)
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
        userlist = whoelse(self)
        for u in userlist:
          self.clientSocket.sendall(u.encode())
  
  def upgradeConnection(self, contents: dict):

    # args
    username, password = contents['user'], contents['password']

    # packing username and password
    # into a tuple
    creds = (username, password)

    '''
    checks if user is already registered
    in the non persisted memory
    '''
    exists = userExists(creds)
    if not exists:
      # create new user object
      new_user = User(username, password)
      # assign user to this thread, to use for method forwarding
      self.user = new_user
      # appending new user in the non persisted storage
      addAllUsers(new_user)
      # appending this thread to online_users
      addOnlineUsers(self)
    else:
      # already exists
      # get user from global all_users list
      user = getSpecificUser(creds)
      # assigning user to this thread, to use for future method forwarding
      self.user = user
      # appending this thread to online_users
      addOnlineUsers(self)










        



    


