"""
    Python 3
    Usage: python3 client.py localhost 8080
    coding: utf-8
"""

from socket import *
import sys
import json

# utils
from util.packetParser import dumpsPacket, loadsPacket

# Client Imports
from Client.auth import loginHandler, registerHandler
from Client.inputThread import InputThread

# exceptions
from exceptions.AuthExceptions import UserNotFoundException

if __name__ == '__main__':

  if len(sys.argv) != 3:
    print("\n===== Error usage, python3 client.py SERVER_IP SERVER_PORT ======\n")
    exit(0)

  '''
  config and ports
  '''

  serverHost = sys.argv[1]
  serverPort = int(sys.argv[2])
  serverAddress = (serverHost, serverPort)


  # define a socket for the client side, it would be used to communicate with the server
  clientSocket = socket(AF_INET, SOCK_STREAM)

  # build connection with the server and send message to it
  clientSocket.connect(serverAddress)


  '''
    authenticate
  '''
  authenticated: bool = False
  username = input("Username: ")
  try:
    tries = 1
    while(not authenticated and tries <= 3):
      authenticated = loginHandler(clientSocket, username)
      tries+=1
  except UserNotFoundException as e:
    authenticated = registerHandler(clientSocket, username)

  '''
    this loop only starts running
    when the client is authenticated
  '''

  
  if authenticated:
    print("Welcome to the greatest messaging application ever!")
    inputThread = InputThread(clientSocket)
    '''
      create new thread to listens to responses if there isnt message input
    '''
    inputThread.start()

    # response = clientSocket.recv(1024)


clientSocket.close()