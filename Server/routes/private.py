from util.Request import sendAndWaitTimeout2, sendAndWait
from util.packetParser import extractContentsToDict, loadsPacket, dumpsPacket
from Server.storage import getOnlineUsers
from Server.routes.block import hasblocked
import json
import select

from exceptions.PrivateExceptions import CannotEstablishPrivateWithSelfException, PrivateConnectionAlreadyExistsException
from exceptions.MessageExceptions import UserHasBeenBlockedException
from exceptions.AuthExceptions import UserNotFoundException

def startPrivateHandler(clientThread, contents: dict):
  '''
    run by origin (initiating) clientThread
    sends to target Client
    {
      message : _message,
      origin : _origin_user
    }
  '''

  target = contents['target']

  target_user = list(filter(lambda u: u.user.getUsername() == target, getOnlineUsers()))

  try:
    target_user = target_user[0]
  except IndexError:
    raise UserNotFoundException

  # check if target_is self
  if target_user == clientThread:
    raise CannotEstablishPrivateWithSelfException

  #TODO check if connection already exists

  # check if target has blocked user
  if hasblocked(clientThread.user, target_user.user):
    raise UserHasBeenBlockedException
 

  edge = {'v1': clientThread.user.getUsername(), 'v2': target_user.user.getUsername()}
  clientThread.p2p.append(edge)
  data = {'message': clientThread.user.getUsername()+" would like to private message, enter y or n: ", 'origin': clientThread.user.getUsername()}
  target_user.clientSocket.sendall(dumpsPacket("P2P", json.dumps(data)).encode())
  
  #add edge to targetuser too
  #target_user.addEdge(edge)
  
  
