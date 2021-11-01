'''
global storage for data structure i.e. dictionaries/arrays
'''

'''
List<ClientThread>
'''
online_users = []

'''
List<User>
'''
all_users = []


'''
List<User>
banned from logging on for next n seconds
stores in user, banned time
'''
timedout_users = []



'''
helper functions
'''

def userExists(user: tuple) -> bool:
  '''
  Checks user exist in all_users global array
  '''
  username, password = user
  for u in all_users:
    if u.checkCredentials(username, password):
      return True
  
  return False


def userOnline(user: tuple) -> bool:
  '''
  Checks users exists in online_users global array

  online_users = List<ClientThread>
  assumptions: ClientThread must include .User
  '''


  username, password = user
  for u in online_users:
    # print(username)
    # print(password)
    # print(u.user.getUsername())
    # print(u.user.getPassword())
    if u.user.checkCredentials(username, password):
      return True

  return False



'''
Methods for online_users
'''

def getOnlineUsers():
  global online_users
  return online_users

def addOnlineUsers(thread):
  '''
  Adding new ClientThread object
  to online_users
  '''
  global online_users
  online_users.append(thread)

def setUserOffline(thread):
  '''
  Removes ClientThread from online_users array
  '''
  global online_users
  online_users = list(filter(lambda x: x != thread, online_users))




'''
Methods for all_users
'''
def getAllusers():
  global all_users
  return all_users


def addAllUsers(user):
  '''
  Appends user from all_user list
  Once added does not get removed
  '''
  global all_users
  all_users.append(user)


def getSpecificUser(user: tuple):
  '''
  Returns User if credential matches
  '''
  username, password = user
  for u in all_users:
    if u.checkCredentials(username, password):
      return u

'''
methods for timed out users
'''
def userTimedOut(user: tuple) -> bool:
  username, password = user
  for u in timedout_users:
    if(u.checkCredentials(username, password) and u.isTimedOut()):
      return True
  return False


def addUserTimeOut(user):
  timedout_users.append(user)