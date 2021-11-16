import time
from exceptions.BlockExceptions import UserAlreadyBlockedException, UserNotAlreadyBlockedException

from Server.config import BLOCK_DURATION
'''
This class is the main user class

'''

class User():
  def __init__(self, username, password):
    self.__username = username
    self.__password = password
    self.__bannedTime = None


    '''
      will store in dumpsPacket format
      [200] _sender: _message
      and will be easily sent 
    '''
    self.__messageQueue = []

    '''
      list of users that are blocked from sending 
      the user any messages

      List<User>
    '''
    self.__blocklist = []
  
  def getUsername(self):
    return self.__username
  
  def getPassword(self):
    return self.__password

  def checkCredentials(self, user: str, password: str) -> bool:
    if self.getUsername() == user and self.getPassword() == password:
      return True
    return False
  
  def setBannedTime(self,time):
    self.__bannedTime = time
  
  def isTimedOut(self):
    if(self.__bannedTime != None):
      # time lapsed
      if(time.time() - self.__bannedTime <= BLOCK_DURATION):
        return True
    return False
  
  '''
    offline message functions
  '''

  def queueMessage(self, message):
    self.__messageQueue.append(message)
  
  def dequeueMessage(self):
    return self.__messageQueue.pop(0)

  '''
    block functions
  '''

  def blockUser(self, user):
    '''
      Raises Exception if user is already blocked
    '''
    if user not in self.__blocklist:
      self.__blocklist.append(user)
    else:
      raise UserAlreadyBlockedException

  def unblockUser(self, user):
    '''
      Raises Exception if user not found in block list
    '''
    for i,u in enumerate(self.__blocklist):
      if u.getUsername() == user.getUsername():
        self.__blocklist.pop(i)
        return
    
    raise UserNotAlreadyBlockedException
  
  def getBlocked(self):
    return self.__blocklist