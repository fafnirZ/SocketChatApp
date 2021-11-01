import time
'''
This class is the main user class
TODO 

'''

class User():
  def __init__(self, username, password):
    self.__username = username
    self.__password = password
    self.__bannedTime = None
  
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
      if(time.time() - self.__bannedTime <= 10):
        print(time.time())
        print(self.__bannedTime)
        return True
    return False