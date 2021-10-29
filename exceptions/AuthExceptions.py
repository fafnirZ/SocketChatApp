
class UserNotFoundException(Exception):
  pass


class InvalidCredentialsException(Exception):
  pass

class UserAlreadyOnlineException(Exception):
  pass

class UserTimedOutException(Exception):
  pass