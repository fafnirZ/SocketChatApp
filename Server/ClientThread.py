from threading import Thread
import time

# Server Imports

from Server.routes.auth import loginHandler, registerHandler
from Server.routes.whoelse import whoelse
from Server.routes.timeout import checkUserLoggedIn, checkUserTimedOut

from Server.storage import userOnline, userExists, addOnlineUsers, addAllUsers, setUserOffline, addUserTimeOut
from Server.User import User

#utils
from util.packetParser import dumpsPacket


# exceptions from root dir
from exceptions.AuthExceptions import UserNotFoundException, UserAlreadyOnlineException,UserTimedOutException, InvalidCredentialsException
from exceptions.InputExceptions import InvalidInputException

# utils from root dir
from util.packetParser import loadsPacket, extractContentsToDict

class ClientThread(Thread):
  
  def __init__(self, clientAddress, clientSocket):
    # super()
    Thread.__init__(self)
    self.clientAddress = clientAddress
    self.clientSocket = clientSocket
    self.clientActive = False

    # max attempts before timeout
    self.max_attempts = 3
    # initialises failed attempts as 0
    self.attempts = 0

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
        
        '''
        only checks if there is a password in the contents
          check if user is already online or blocked
          TODO handle automatically removing user from blocked
        '''
        if('password' in contents):
          err = self.checkAuthExceptions(contents)
          if(err):
            # break or exit
            break

        '''
        handle invalid credentials
        '''
        try:
          logged = loginHandler(contents, self.clientSocket)
        except InvalidCredentialsException as e:
          self.attempts += 1
          if self.attempts >= self.max_attempts:
            # block user
            user = User(contents['user'], contents['password'])
            user.setBannedTime(time.time())
            addUserTimeOut(user)

            # send to frontend
            response = dumpsPacket(403, "Invalid Password. Your account has been blocked. Please try again later").encode('utf-8')
            self.clientSocket.sendall(response)
          else:
            # todo handle exceptions and send back to client
            response = dumpsPacket(401, "Invalid Credentials").encode('utf-8')
            self.clientSocket.sendall(response)


        # since logged in, that means username and password is provided correctly
        if logged:
          self.upgradeConnection(contents)
      
      elif code == "register":
        contents = extractContentsToDict(contents)
        logged = registerHandler(contents, self.clientSocket)

        if logged:
          self.upgradeConnection(contents)

      elif code == "whoelse":
        userlist = whoelse(self)
        for u in userlist:
          self.clientSocket.sendall(u.encode())

  
  
  def upgradeConnection(self, contents: dict):

    # args
    username, password = contents['user'], contents['password']

    # packing username and password
    # into a tuple
    creds = (username, password)
    print("upgraded")
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

  def checkAuthExceptions(self, contents:dict) -> bool:
    try:
      checkUserLoggedIn(contents)
      checkUserTimedOut(contents)
    except UserAlreadyOnlineException as e:
      response = dumpsPacket(401, "User already online").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      return True
    except UserTimedOutException as e:
      response = dumpsPacket(403, "Your account is blocked due to multiple login failures. Please try again later").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      return True

    # return false if no exception has been raised
    return False










        



    


