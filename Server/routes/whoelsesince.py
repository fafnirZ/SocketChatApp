from Server.log import getLog
from Server.routes.block import hasblocked
import time

def whoelsesince(thread, contents) -> list:
  '''
  '''
  logs = getLog()
  time_before = int(contents['time'])

  filtered = []
  for i in logs:
    if(i['thread'] is not thread and time.time() - i['time'] <= time_before):

      # only show those who have not blocked user
      if(hasblocked(thread.user, i['thread'].user) == False):
        filtered.append(i['thread'].user.getUsername())

  # remove duplicates
  filtered = list(set(filtered))
  return filtered
