from Server.storage import getOnlineUsers

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
    print(dumpsPacket(200,message))
    user.clientSocket.sendall(dumpsPacket(200, message).encode('utf-8'))