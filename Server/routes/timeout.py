from exceptions.AuthExceptions import UserAlreadyOnlineException, UserTimedOutException
from Server.storage import userOnline, userTimedOut

'''
  check if client is already logged in
'''

def checkUserLoggedIn(content:dict):
  online = userOnline((content['user'], content['password']))
  if (online):
    raise UserAlreadyOnlineException

'''
  check if user is in timeout list
'''
def checkUserTimedOut(content: dict)->bool:
  if(userTimedOut((content['user'], content['password']))):
    raise UserTimedOutException