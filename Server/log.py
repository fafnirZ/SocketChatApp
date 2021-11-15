import time
from util.mutex import mutex

'''
log history containing clientThreads
List<ClientThread>
'''
log = []

def getLog():
  return log

def logUser(user):
  mutex.acquire()
  log.append({'thread': user, 'time': time.time()})
  mutex.release()