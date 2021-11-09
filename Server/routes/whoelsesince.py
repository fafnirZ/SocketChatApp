from Server.log import getLog
import time

def whoelsesince(thread, time) -> list:
  '''
  '''

  time_before = int(time)

  filtered = list(filter(lambda x: time.time()-int(x['time']) <= time_before, getLog()))
  print(filtered)
