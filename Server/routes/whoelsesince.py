from Server.log import getLog
import time

def whoelsesince(thread, contents) -> list:
  '''
  '''
  logs = getLog()
  time_before = int(contents['time'])
  # time_before = int(time)

  #filtered = list(filter(lambda x: time.time()-int(x['time']) <= time_before, logs))
  filtered = []
  for i in logs:
    if(i['thread'] is not thread and time.time() - i['time']):
      filtered.append(i['thread'].user.getUsername())

  # remove duplicates
  filtered = list(set(filtered))
  return filtered
