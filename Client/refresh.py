from util.packetParser import dumpsPacket
from util.Request import post

def refreshTimer(open_sockets):
  skt = None
  for sockt in open_sockets:
    if sockt['connection'] == 'server':
      skt = sockt['socket']
  if(skt != None):
    post(skt, "refresh", {})

