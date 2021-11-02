import os
import threading
'''
functions for interacting with credentials file
'''

def saveCredentials(user:str, password: str):
  '''
  saves credentials to the credentials.txt file
  '''
  with open(os.path.dirname(__file__)+'/credentials.txt', 'a') as f:
    f.write(f"\n{user} {password}")



def getAllCredentials() -> list:
  '''
  get all credentials in credential file
  '''
  l = []
  with open(os.path.dirname(__file__)+'/credentials.txt', 'r') as f:
    for line in f:
      l.append(line.rstrip())
  return l


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