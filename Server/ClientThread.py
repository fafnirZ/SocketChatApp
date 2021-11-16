from threading import Thread
import threading
import time

# Server Imports

from Server.routes.auth import loginHandler, registerHandler
from Server.routes.whoelse import whoelse
from Server.routes.whoelsesince import whoelsesince
from Server.routes.timeout import checkUserLoggedIn, checkUserTimedOut
from Server.routes.broadcast import broadcastHandler
from Server.routes.message import messageHandler
from Server.routes.block import blockHandler, unblockHandler
from Server.timer import Timer
from Server.log import logUser


from Server.storage import userOnline, userExists, addOnlineUsers, addAllUsers, setUserOffline, addUserTimeOut, getSpecificUser, online_users, all_users
from Server.User import User

#utils
from util.packetParser import dumpsPacket


# exceptions from root dir
from exceptions.AuthExceptions import UserNotFoundException, UserAlreadyOnlineException, UserTimedOutException, InvalidCredentialsException
from exceptions.InputExceptions import InvalidInputException
from exceptions.MessageExceptions import UserHasBeenBlockedException
from exceptions.BlockExceptions import UserAlreadyBlockedException, CannotBlockSelfException, UserNotAlreadyBlockedException

# utils from root dir
from util.packetParser import loadsPacket, extractContentsToDict

class ClientThread(Thread):

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


  def sendToClient(fnc):
    def wrapper(self, *args):
      resp = fnc(self, *args)
      self.clientSocket.sendall(resp)
    return wrapper
  
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

    # terminateEvent
    self.terminateEvent = threading.Event()

    # adding user login to log history
    logUser(self)
  
  def run(self):
    # initialise countdown inactivity timer
    self.timer = Timer(callback=self.clientCleanUp)

    message = ''
    # start inactivity timer
    self.timer.start()

    while self.clientActive:
      data = self.clientSocket.recv(1024)
      message = data.decode()

      '''
      if message from client is empty
      client is offline
      '''
      if message == '':
        # terminate timer
        # timer.forcequit causes timer callback function to not run
        self.timer.forcequit()
        '''
          only run this is the thread has not been terminated already
          this fixes the double terminate broadcast issue 
        '''
        if not self.terminateEvent.is_set():
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
          # if error will quit the run loop
          break

      elif code == "register":
        self.register(contents)

      elif code == "whoelse":
        self.whoelse(contents)

      elif code == "whoelsesince":
        self.whoelsesince(contents)
      
      elif code == "broadcast":
        self.broadcast(contents)
      
      elif code == "message":
        self.message(contents)
      
      elif code == "block":
        self.block(contents)
      
      elif code == "unblock":
        self.unblock(contents)

  
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

    # dequeue any messages that were sent to user while offline
    self.deQueueMessages()

  '''
    helper function for checking and handling the exceptions
    for user authentication
  '''
  def checkAuthExceptions(self, contents:dict) -> bool:
    try:
      checkUserLoggedIn(contents)
      checkUserTimedOut(contents)
    except UserAlreadyOnlineException as e:
      response = dumpsPacket(403, "User already online\n").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      # 403 causes client to exit
      return True
    except UserTimedOutException as e:
      response = dumpsPacket(403, "Your account is blocked due to multiple login failures. Please try again later\n").encode('utf-8')
      self.clientSocket.sendall(response)
      # send signal to client to exit
      # 403 causes client to exit
      return True

    # return false if no exception has been raised
    return False

  '''
    cleanup function
  '''
  @sendToClient
  def clientCleanUp(self):

    # sets self.terminateEvent is true
    self.terminateEvent.set()

    self.clientActive = False
    print("===== the user disconnected - ", self.clientAddress)
    
    # broadcasts that the user has logged
    broadcastHandler(self, self.user.getUsername()+" has logged out\n")

    # removes current thread from list of threads in online_users
    setUserOffline(self)

    # send a packet to client to kick client due to inactivity
    return dumpsPacket("FIN", "Your client has been closed due to inactivity").encode('utf-8')

  '''
    route methods
  '''
  @resetTimer
  def login(self, contents) -> bool:
    contents = extractContentsToDict(contents)
    logged = False
        
    '''
      only checks if there is a password in the contents
      check if user is already online or banned
      TODO handle automatically removing user from banned
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
  @sendToClient
  def register(self, contents):
    contents = extractContentsToDict(contents)
    logged = registerHandler(contents, self.clientSocket)
    response = dumpsPacket(200, None).encode('utf-8')

    if logged:
      self.upgradeConnection(contents)
    
    return response

  @resetTimer
  @sendToClient
  def whoelse(self, contents):
    userlist = whoelse(self)
    response = ""
    for u in userlist:
      resp = u + "\n"
      response += resp
    return dumpsPacket(200, response).encode('utf-8')

  
  @resetTimer
  @sendToClient
  def whoelsesince(self, contents):
    contents = extractContentsToDict(contents)
    userlist = whoelsesince(self, contents)
    response = ""
    for u in userlist:
      resp = u + "\n"
      response += resp
    return dumpsPacket(200, response).encode('utf-8')
  
  @resetTimer
  @sendToClient
  def broadcast(self, contents):
    contents = extractContentsToDict(contents)
    broadcastHandler(self, self.user.getUsername() + ": " + contents['message']+"\n")
    return dumpsPacket(200, "").encode()

  @resetTimer
  @sendToClient
  def message(self, contents):
    contents = extractContentsToDict(contents)
    try:
      messageHandler(self, contents)
    except UserHasBeenBlockedException:
      return dumpsPacket(400, "Error. Your message could not be delivered as the recipient has blocked you\n").encode()
    except UserNotFoundException:
      return dumpsPacket(400, "Error. User not found\n").encode()
    # let original client know it is done
    return dumpsPacket(200, "").encode()

  '''
    should occur after user has upgraded connection
  '''
  def deQueueMessages(self):
    '''
      when user logs on, the all messages in message queue
      will be displayed
    '''
    response = ""
    try:
      msg = self.user.dequeueMessage()
      while(msg):
        # send to frontend
        print(msg)
        self.clientSocket.sendall(msg.encode('utf-8'))
        # get more messages
        msg = self.user.dequeueMessage()
    except:
      pass
    
  @resetTimer
  @sendToClient
  def block(self, contents):
    contents = extractContentsToDict(contents)
    try:
      blockHandler(self, contents)
    except CannotBlockSelfException:
      return dumpsPacket(400, f"Error. Cannot Block Self\n").encode()
    except UserNotFoundException:
      return dumpsPacket(400, f"Error. {contents['block']} cannot be found\n").encode()
    except UserAlreadyBlockedException:
      return dumpsPacket(400, f"Error. {contents['block']} is already blocked\n").encode()

    # else
    return dumpsPacket(200, f"{contents['block']} is blocked\n").encode()
  
  @resetTimer
  @sendToClient
  def unblock(self, contents):
    contents = extractContentsToDict(contents)
    try:
      unblockHandler(self, contents)
    except UserNotAlreadyBlockedException:
      return dumpsPacket(400, f"Error. {contents['unblock']} was not blocked\n").encode()
    return dumpsPacket(200, f"{contents['unblock']} is unblocked\n").encode()
