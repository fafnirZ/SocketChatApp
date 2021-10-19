import os
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