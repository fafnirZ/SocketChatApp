from util.Request import sendAndWaitTimeout2
from util.packetParser import extractContentsToDict
from Server.storage import getOnlineUsers

def startPrivateHandler(clientThread, contents: dict):
  target = contents['target']

  target_user = list(filter(lambda u: u.user.getUsername() == target, getOnlineUsers()))

  target_user = target_user[0]

  resp = sendAndWaitTimeout2(target_user.clientSocket, "P2P", clientThread.user.getUsername()+" would like to private message, enter y or n: ")

  contents = extractContentsToDict(resp)
  print(contents)
