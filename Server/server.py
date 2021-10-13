"""
    Usage: python3 server.py localhost 8080
    coding: utf-8

"""
from socket import *
from threading import Thread
import sys, select

#utils
from config import serverSocket
from ClientThread import ClientThread



if __name__ == '__main__':

  '''
  invalid argv error
  '''
  if len(sys.argv) != 3:
    print("\n===== Error usage, python3 server.py SERVER_HOST SERVER_PORT ======\n")
    exit(0)

  '''
  main loop
  '''
  while True:
    serverSocket.listen()
    clientSocket, clientAddress = serverSocket.accept()
    # client socket and client address
    clientThread = ClientThread(clientAddress, clientSocket)
    clientThread.start()

  
  # close sockets
  serverSocket.close()