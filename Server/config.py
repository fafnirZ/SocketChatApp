import sys
from socket import *

SERVER_HOST = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
BLOCK_DURATION = int(sys.argv[3])
TIMEOUT = int(sys.argv[4])

'''
server socket to be exported
'''

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(SERVER_ADDRESS)
