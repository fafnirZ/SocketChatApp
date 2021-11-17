from threading import Thread
from socket import *

class P2PThread(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.clientActive = True
  
  def run(self):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', 0))
    sock.listen()
    sockt, addr = sock.accept()

    self.P2PSocket = sockt
    self.P2PAddress = addr
    while self.clientActive:

      data = self.P2PSocket.recv(1024)
      print(data)
      if message == '':
        break
  
  def getClientAddress(self):
    return self.P2PAddress
  
  def getClientSocket(self):
    return self.P2PSocket