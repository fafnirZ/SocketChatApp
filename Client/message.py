from util.Request import post

def messageHandler(socket, command: str):
  '''
    command: message _user _message
    format:
    {
      'reciever': _user,
      'message': _message
    }
    packet format:
    [message] {'reciever':_user, 'message':_message}

    response format:
    [200] ""

    error format:
    [400] user has blocked you
  '''
  command = command.split(" ")
  reciever = command[1]
  message = " ".join(command[2:])

  post(socket, 'message', {'reciever': reciever, 'message': message})