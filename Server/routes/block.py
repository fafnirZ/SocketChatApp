from Server.storage import getAllusers, getUserByName

#exceptions
from exceptions.AuthExceptions import UserNotFoundException
from exceptions.BlockExceptions import CannotBlockSelfException

#utils
from util.packetParser import dumpsPacket

def blockHandler(clientThread, contents):
  '''
    expecting
    {'block' : _username}
  '''
  ALL_users = getAllusers()
  block = contents['block']
  target_user = list(filter(lambda u: u.getUsername() == block, ALL_users))

  if len(target_user)<1:
    raise UserNotFoundException

  for user in target_user:
    if(user == clientThread.user):
      raise CannotBlockSelfException

    clientThread.user.blockUser(user)



def unblockHandler(clientThread, contents):
  '''
    expecting
    {'unblock' : _username}
  '''
  ALL_users = getAllusers()
  unblock = contents['unblock']
  target_user = list(filter(lambda u: u.getUsername() == unblock, ALL_users))

  for user in target_user:
    clientThread.user.unblockUser(user)



def hasblocked(sender, reciever):
  '''
    checks if the reciever has blocked the sender
  '''
  for user in reciever.getBlocked():
    if user == sender:
      return True
  return False