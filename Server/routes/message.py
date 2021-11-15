from Server.storage import getOnlineUsers

#utils
from util.packetParser import dumpsPacket

def messageHandler(clientThread, contents):
  '''
    expecting 
    {'reciever': , 'message': }
  '''
  online_users = getOnlineUsers()
  target_user = list(filter(lambda x: x.user.getUsername() == contents['reciever'], online_users))

  message = contents['message']
  current_user = clientThread.user.getUsername()
  for user in target_user:
    print(dumpsPacket(200,message))
    user.clientSocket.sendall(dumpsPacket(200, current_user+': '+message+"\n").encode('utf-8'))

