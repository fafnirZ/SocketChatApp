import time
import threading

'''
log history containing clientThreads
List<ClientThread>
'''
log = []

'''
mutex
'''
mutex = threading.Lock()

def getLog():
  return log

def logUser(user):
  mutex.acquire()
  log.append({'thread': user, 'time': time.time()})
  mutex.release()