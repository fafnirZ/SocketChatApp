import socket
import time


def recv_timeout(socket, timeout=2):
  socket.setblocking(0)
  begin = time.time()
  total_data = []
  while 1:
    if time.time()-begin > timeout:
      break
    try:
      data = socket.recv(1024)
      if data:
        total_data.append(data.decode())
        begin=time.time()
      else:
        time.sleep(0.1)
    except:
      pass
  return ''.join(total_data)
  