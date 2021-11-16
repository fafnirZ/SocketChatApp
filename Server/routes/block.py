from Server.storage import getAllusers, getUserByName

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

  for user in target_user:
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


