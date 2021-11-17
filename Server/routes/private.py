from util.Request import sendAndWaitTimeout2, sendAndWait
from util.packetParser import extractContentsToDict, loadsPacket, dumpsPacket
from Server.storage import getOnlineUsers
import json
import select

from exceptions.PrivateExceptions import CannotEstablishPrivateWithSelfException, PrivateConnectionAlreadyExistsException

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

  target_user = target_user[0]


  # check if target_is self
  if target_user == clientThread:
    raise CannotEstablishPrivateWithSelfException

  # check if connection already exists
  

  '''
    non blocking socket
  '''
  # resp = None
  # s = target_user.clientSocket
  # s.sendall(dumpsPacket("P2PDUPE", json.dumps(data)).encode())
  # s.setblocking(0)
  # flag = 1
  # while flag:
  #   readable, _, _ = select.select([s],[s],[],0.5)
  #   for s in readable:
  #     resp = s.recv(1048)
  #     flag = 0
  # s.setblocking(1)

  #resp = sendAndWait(target_user.clientSocket, "P2PDUPE", data)
  # target_user.clientSocket.sendall(dumpsPacket("P2PDUPE", json.dumps(data)).encode())
  # print(target_user)
  # resp = target_user.get200()
  # print(resp)
  
  # print("after")

  # print(resp)
  # code , contents = loadsPacket(resp.decode())
  # if code == "400":
  #   raise PrivateConnectionAlreadyExistsException

  edge = {'v1': clientThread.user.getUsername(), 'v2': target_user.user.getUsername()}
  clientThread.p2p.append(edge)
  data = {'message': clientThread.user.getUsername()+" would like to private message, enter y or n: ", 'origin': clientThread.user.getUsername()}
  target_user.clientSocket.sendall(dumpsPacket("P2P", json.dumps(data)).encode())
  
  #add edge to targetuser too
  target_user.addEdge(edge)
  
  #non blockingish send and wait 
  # s.setblocking(0)
  # flag = 1
  # while flag:
  #   readable, writable, _ = select.select([s],[s],[],0.5)
  #   for s in writable:
  #     s.sendall(dumpsPacket("P2P", json.dumps(data)).encode())
    
  #   for s in readable:
  #     resp = s.recv(1048)
  #     flag = 0
  # s.setblocking(1)

  #code, contents = loadsPacket(resp)

  #print('3')
  #contents = extractContentsToDict(contents)

  # if code == "200":
  #   # sending to client
  #   username = target_user.user.getUsername()
  #   data = contents
  #   data['username'] = username
  #   return dumpsPacket("P2PCONN", json.dumps(data)).encode()
  
  # elif code == "400":
  #   return dumpsPacket(400, f"{target_user.user.getUsername()} has declined your private invitation\n").encode()
