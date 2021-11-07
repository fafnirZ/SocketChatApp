import threading

class Timer(threading.Thread):
  def __init__(self, timeout=15, callback=None):
    threading.Thread.__init__(self)
    self.timeout = timeout

    if callback == None:
      self.callback = None
    else:
      self.callback = callback
    

    self.terminateEvent = threading.Event()
    self.startEvent = threading.Event()
    self.resetEvent = threading.Event()
    self.count = timeout


  def run(self):
    # start timer when initialised
    self.startEvent.set()

    while not self.terminateEvent.is_set():
      while self.count > 0 and self.startEvent.is_set():
        self.count -=1
        if self.resetEvent.wait(1):
          self.resetEvent.clear()
          self.count = self.timeout
      
      # @precondition count <= 0
      # happens after the while loop
      self.startEvent.clear()
      self.callback()
      self.count = self.timeout
      self.terminate()
  
  def reset(self):
    if self.startEvent.is_set():
      self.resetEvent.set()
    else:
      self.startEvent.set()

  def terminate(self):
    self.terminateEvent.set()