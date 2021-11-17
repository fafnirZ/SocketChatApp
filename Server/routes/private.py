from util.Request import sendAndWaitTimeout2, sendAndWait
from util.packetParser import extractContentsToDict, loadsPacket, dumpsPacket
from Server.storage import getOnlineUsers
import json

from exceptions.PrivateExceptions import CannotEstablishPrivateWithSelfException, PrivateConnectionAlreadyExistsException

def startPrivateHandler(clientThread, contents: dict):


  target = contents['target']

  target_user = list(filter(lambda u: u.user.getUsername() == target, getOnlineUsers()))

  target_user = target_user[0]

  # check if target_is self
  if target_user == clientThread:
    raise CannotEstablishPrivateWithSelfException

  # check if connection already exists
  data = {'username': clientThread.user.getUsername()}
  resp = sendAndWait(target_user.clientSocket, "P2PDUPE", data)
  code , contents = loadsPacket(resp)
  if code == "400":
    raise PrivateConnectionAlreadyExistsException

  data = {'message': clientThread.user.getUsername()+" would like to private message, enter y or n: "}
  resp = sendAndWait(target_user.clientSocket, "P2P", data)

  code, contents = loadsPacket(resp)

  contents = extractContentsToDict(contents)

  if code == "200":
    # sending to client
    username = target_user.user.getUsername()
    data = contents
    data['username'] = username
    return dumpsPacket("P2PCONN", json.dumps(data)).encode()
  
  elif code == "400":
    return dumpsPacket(400, f"{target_user.user.getUsername()} has declined your private invitation\n").encode()
