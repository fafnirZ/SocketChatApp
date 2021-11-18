from util.packetParser import dumpsPacket
from util.Request import post
import json

def refreshTimer(open_sockets):
  skt = None
  for sockt in open_sockets:
    if sockt['connection'] == 'server':
      skt = sockt['socket']
  if(skt != None):
    skt.sendall(dumpsPacket("refresh", json.dumps({})+"\n").encode())

