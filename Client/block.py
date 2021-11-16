from util.Request import post

def blockHandler(socket, command: str):
  '''
    command: block _user
    format:
    {
      'block': _user
    }
    packet format:
    [block] {'block': _user}

    response format:
    [200] _user is blocked

    error format:
    [400] Error. _user has already been blocked
    [400] Error. _user not found
    [400] Error. cannot block self
  '''
  command = command.split(" ")
  user = command[1]

  post(socket, 'block', {'block': user})


def unblockHandler(socket, command: str):
  '''
    command: unblock _user
    format:
    {
      'unblock': _user
    }
    packet format:
    [block] {'block': _user}

    response format:
    [200] ""

    error format:
    [400] Error. _user was not blocked
  '''
  command = command.split(" ")
  user = command[1]

  post(socket, 'unblock', {'unblock': user})