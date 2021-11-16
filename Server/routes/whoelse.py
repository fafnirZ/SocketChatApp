# why can i use storage instead of ../storage?
# because the dir structure is from the __name__==__main__ file
# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
from Server.storage import getOnlineUsers
from Server.routes.block import hasblocked

def whoelse(thread) -> list:
  '''
  Args: ClientThread
  Returns every other user who is online at the current time
  '''
  not_current_thread = list(filter(lambda t: t != thread, getOnlineUsers()))
  not_blocked_user = list(filter(lambda t: hasblocked(thread.user, t.user) == False, not_current_thread))
  usernames = list(map(lambda t: t.user.getUsername(), not_blocked_user))
  return usernames