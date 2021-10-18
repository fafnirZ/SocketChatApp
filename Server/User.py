'''
This class is the main user class
TODO 

'''

class User():
  def __init__(self, username, password):
    self.__username = username
    self.__password = password
  
  def getUsername(self):
    return self.__username
  
  def getPassword(self):
    return self.__password

  def checkCredentials(self, user: str, password: str) -> bool:
    if self.getUsername() == user and self.getPassword == password:
      return True
    return False