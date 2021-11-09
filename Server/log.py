import time

'''
log history containing clientThreads
List<ClientThread>
'''
log = []

def getLog():
  return log

def logUser(user):
  log.append({'thread': user, 'time': time.time()})