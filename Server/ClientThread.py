from threading import Thread
import time

# Server Imports

from Server.routes.auth import loginHandler, registerHandler
from Server.routes.whoelse import whoelse
from Server.routes.whoelsesince import whoelsesince
from Server.routes.timeout import checkUserLoggedIn, checkUserTimedOut
from Server.routes.broadcast import broadcastHandler
from Server.timer import Timer
from Server.log import logUser


from Server.storage import userOnline, userExists, addOnlineUsers, addAllUsers, setUserOffline, addUserTimeOut, getSpecificUser
from Server.User import User

#utils
from util.packetParser import dumpsPacket


# exceptions from root dir
from exceptions.AuthExceptions import UserNotFoundException, UserAlreadyOnlineException, UserTimedOutException, InvalidCredentialsException
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

    # initialise countdown inactivity timer
    self.timer = Timer(callback=self.clientCleanUp)

    print('=== New connection for: ', clientAddress)
    self.clientActive = True

    # adding user login to log history
    logUser(self)
  
  def run(self):
    message = ''
    # start inactivity timer
    self.timer.start()

    while self.clientActive:
      data = self.clientSocket.recv(1024)
      message = data.decode()

      # print(f"message: {message}")

      '''
      if message from client is empty
      client is offline
      '''
      if message == '':
        self.clientCleanUp()
        break

      '''
      parses the message to a readable format
      and handle the different commands
      '''
      (code, contents) = loadsPacket(message)

      if code == "login":
        err = self.login(contents)
        if err:
          break
      

      elif code == "register":
        self.register(contents)

      elif code == "whoelse":
        self.whoelse(contents)

      elif code == "whoelsesince":
        self.whoelsesince(contents)
      
      elif code == "broadcast":
        self.broadcast(contents)


  
  '''
    upgrades connection
  '''
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
    
    # presence broadcast for login
    broadcastHandler(self, self.user.getUsername()+ " has logged in\n")

  '''
    helper function for checking and handling the exceptions
    for user authentication
  '''
  def checkAuthExceptions(self, contents:dict) -> bool:
    try:
      checkUserLoggedIn(contents)
      checkUserTimedOut(contents)
    except UserAlreadyOnlineException as e:
      response = dumpsPacket(403, "User already online").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      # 403 causes client to exit
      return True
    except UserTimedOutException as e:
      response = dumpsPacket(403, "Your account is blocked due to multiple login failures. Please try again later").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      # 403 causes client to exit
      return True

    # return false if no exception has been raised
    return False

  '''
    cleanup function
  '''
  def clientCleanUp(self):
    self.clientActive = False
    print("===== the user disconnected - ", self.clientAddress)
    
    # broadcasts that the user has logged
    broadcastHandler(self, self.user.getUsername()+" has logged out")

    # removes current thread from list of threads in online_users
    setUserOffline(self)

    # send a packet to client to kick client due to inactivity
    self.clientSocket.sendall(dumpsPacket("FIN", "Your client has been closed due to inactivity").encode('utf-8'))


  '''
    decorator for resetting
    timer after each valid user route call
  '''
  def resetTimer(fnc):
    def wrapper(self,*args):
      self.timer.reset()
      fnc(self,*args)
      self.timer.reset()
      print('inactivity reset')
    return wrapper


  '''
    route methods
  '''
  @resetTimer
  def login(self, contents) -> bool:
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
        return True

    '''
    handle invalid credentials
    '''
    try:
      '''
      goes into the route handler
      '''
      logged = loginHandler(contents, self.clientSocket)
    except InvalidCredentialsException as e:
      # checking for attempts
      self.attempts += 1
      if self.attempts >= self.max_attempts:
        # block user
        user = User(contents['user'], contents['password'])
        user.setBannedTime(time.time())
        addUserTimeOut(user)

        # send to frontend
        response = dumpsPacket(403, "Invalid Password. Your account has been blocked. Please try again later\n").encode('utf-8')
        self.clientSocket.sendall(response)
      else:
        # todo handle exceptions and send back to client
        response = dumpsPacket(401, "Invalid Credentials\n").encode('utf-8')
        self.clientSocket.sendall(response)


    # since logged in, that means username and password is provided correctly
    if logged:
      self.upgradeConnection(contents)

    return False


  @resetTimer
  def register(self, contents):
    contents = extractContentsToDict(contents)
    logged = registerHandler(contents, self.clientSocket)
    response = dumpsPacket(200, None).encode('utf-8')
    self.clientSocket.sendall(response)

    if logged:
      self.upgradeConnection(contents)

  @resetTimer
  def whoelse(self, contents):
    userlist = whoelse(self)
    for u in userlist:
      resp = u + "\n"
      response = dumpsPacket(200, resp).encode('utf-8')
      self.clientSocket.sendall(response)
  
  @resetTimer
  def whoelsesince(self, contents):
    contents = extractContentsToDict(contents)
    userlist = whoelsesince(self, contents)
    for u in userlist:
      resp = u + "\n"
      response = dumpsPacket(200, resp).encode('utf-8')
      self.clientSocket.sendall(response)
  
  @resetTimer
  def broadcast(self, contents):
    contents = extractContentsToDict(contents)
    broadcastHandler(self, self.user.getUsername() + ": " + contents['message'])
    self.clientSocket.sendall(dumpsPacket(200, None).encode())


