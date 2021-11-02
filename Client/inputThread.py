from threading import Thread

# util
from util.Request import sendAndWait

from Client.broadcast import broadcastHandler

class InputThread(Thread):

  def __init__(self, clientSocket):
    Thread.__init__(self)
    self.clientSocket = clientSocket


  '''
    handling user input
  '''
  def run(self):
    while True:
      message = input()
      
      if message == 'whoelse':
        '''
          Sends this:
          [whoelse] {}
        '''
        
        response = sendAndWait(self.clientSocket, 'whoelse', {})
        # no new line
        #print(response, end="")
      if message.startswith('broadcast'):
        '''
          broadcast message
        '''
        broadcastHandler(self.clientSocket, message)