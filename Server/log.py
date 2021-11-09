import time

'''
log history containing clientThreads
List<ClientThread>
'''
log = []

def getLog():
  return log

def logUser(user):
  log.append({user, time.time()})