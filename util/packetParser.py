import re
import json

'''
requests would be in format
[login], [logout]


responses will be in format
[200], [500]


example request and response

[login] {user: aaa}
[200] success
[login] {user: aaa, password: bbb}
[400] {err :"invalid credentials"}

'''
def loadsPacket(msg: str) -> (str, str):
  l = msg.split(" ")
  # extracting the code
  code = re.search('^\[([a-zA-Z0-9]+)\]', l[0]).group(1)
  content = ' '.join(l[1:])
  
  #TODO raise exception if failed
  return (code, content)


'''
format: [{code}] {content}
'''
def dumpsPacket(code: str, content: str) -> str:
  ret: str = '['+ str(code) + ']' + ' ' + str(content)
  return ret


'''
uses json.loads
'''
def extractContentsToDict(msg : str) -> dict:
  return json.loads(msg)

