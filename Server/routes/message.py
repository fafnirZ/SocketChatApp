from Server.storage import getOnlineUsers, getUserByName
from Server.routes.block import hasblocked

from exceptions.MessageExceptions import UserHasBeenBlockedException

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


  '''
    signifies either
    user is not online
    or user does not exist
  '''
  if len(target_user) < 1:
    # if exists add message to message queue
    user = getUserByName(contents['reciever'])
    if user == None:
      return
    else:
      store = dumpsPacket(200, current_user+': '+message+"\n")
      user.queueMessage(store)

  else:
    for user in target_user:

      '''
        check if reciever has blocked sender
      '''
      if(hasblocked(clientThread.user, user.user)):
        raise UserHasBeenBlockedException
      

      '''
        send message to matches
      '''
      print(dumpsPacket(200,message))
      user.clientSocket.sendall(dumpsPacket(200, current_user+': '+message+"\n").encode('utf-8'))
  
