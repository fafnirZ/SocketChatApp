import threading

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

'''
mutex
'''
mutex = threading.Lock()



def userExists(user: tuple) -> bool:
  mutex.acquire()
  '''
  Checks user exist in all_users global array
  '''
  username, password = user
  for u in all_users:
    if u.checkCredentials(username, password):
      mutex.release()
      return True
  mutex.release()
  
  return False


def userOnline(user: tuple) -> bool:
  mutex.acquire()
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
      mutex.release()
      return True
  mutex.release()
  return False



'''
Methods for online_users
'''

def getOnlineUsers():
  mutex.acquire()
  global online_users
  mutex.release()
  return online_users

def addOnlineUsers(thread):
  '''
  Adding new ClientThread object
  to online_users
  '''
  mutex.acquire()
  global online_users
  mutex.release()
  online_users.append(thread)

def setUserOffline(thread):
  '''
  Removes ClientThread from online_users array
  '''
  mutex.acquire()
  global online_users
  online_users = list(filter(lambda x: x != thread, online_users))
  mutex.release()



'''
Methods for all_users
'''
def getAllusers():
  mutex.acquire()
  global all_users
  mutex.release()
  return all_users


def addAllUsers(user):
  '''
  Appends user from all_user list
  Once added does not get removed
  '''
  mutex.acquire()
  global all_users
  all_users.append(user)
  mutex.release()


def getSpecificUser(user: tuple):
  '''
  Returns User if credential matches
  '''
  mutex.acquire()
  username, password = user
  for u in all_users:
    if u.checkCredentials(username, password):
      return u
  mutex.release()

'''
methods for timed out users
'''
def userTimedOut(user: tuple) -> bool:
  mutex.acquire()
  username, password = user
  for u in timedout_users:
    if(u.checkCredentials(username, password) and u.isTimedOut()):
      mutex.release()
      return True
  mutex.release()
  return False


def addUserTimeOut(user):
  mutex.acquire()
  timedout_users.append(user)
  mutex.release()