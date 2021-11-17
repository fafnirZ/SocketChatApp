from util.Request import sendAndWaitTimeout2, sendAndWait
from util.packetParser import extractContentsToDict, loadsPacket, dumpsPacket
from Server.storage import getOnlineUsers
import json

def startPrivateHandler(clientThread, contents: dict):


  target = contents['target']

  target_user = list(filter(lambda u: u.user.getUsername() == target, getOnlineUsers()))

  target_user = target_user[0]

  data = {'message': clientThread.user.getUsername()+" would like to private message, enter y or n: "}
  resp = sendAndWait(target_user.clientSocket, "P2P", data)

  code, contents = loadsPacket(resp)

  contents = extractContentsToDict(contents)
  # reply = contents['reply']


  # if reply == 'yes':
  #   pass
  # elif reply == 'no':
  #   pass
  if code == "200":
    # sending to client
    username = target_user.user.getUsername()
    data = contents
    data['username'] = username
    clientThread.clientSocket.sendall(dumpsPacket("P2PCONN", json.dumps(data)).encode())
  
  elif code == "400":
    pass