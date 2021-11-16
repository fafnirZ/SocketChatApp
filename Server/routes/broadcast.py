from Server.storage import getOnlineUsers
from Server.routes.block import hasblocked

#utils
from util.packetParser import dumpsPacket


def broadcastHandler(clientThread, message:str):
  online_users = getOnlineUsers()
  online_users = list(filter(lambda x: x != clientThread, online_users))
  '''
    broadcasting message to all online users
    that are not self
  '''
  for user in online_users:
    # will not broadcast to users who have blocked the you
    if(not hasblocked(clientThread.user, user.user)):
      user.clientSocket.sendall(dumpsPacket(200, message).encode('utf-8'))