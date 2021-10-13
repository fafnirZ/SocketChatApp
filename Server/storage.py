'''

global storage for data structure i.e. dictionaries/arrays


'''

online_users = []

all_users = []


def userInList(user: tuple, list: list) -> bool:
  username, password = user
  for u in list:
    if u.getUsername() == username and u.getpassword() == password:
      return True
  
  return False

