from util.Request import post

def startPrivateHandler(socket, command:str):
  '''
    command: startprivate _user
    format:
    {
      'target' : _user
    }
    packet format:
    [message] {'target': _user}

    response format:
    [200] ""

    error format:
    [400] user has declined
    [400] the user has blocked you
    [400] a private connection with user is already established
  '''
  command = command.split(" ")
  target = command[1]

  post(socket, 'startprivate', {'target': target})
  

def replyYes(socket):
  post(socket, 'reply', {'reply': "yes"})

def replyNo(socket):
  post(socket, 'reply', {'reply': "no"})
