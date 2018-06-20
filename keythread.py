import threading
import time
class getb(threading.Thread):
  def __init__ (self,printa):
    threading.Thread.__init__(self)
    self.printa=printa
  def run(self):
    while True:
      k=raw_input()
      if k=="b":
        self.printa.stop=True
        break
class printa(threading.Thread):
  def __init__ (self):
    threading.Thread.__init__(self)
    self.stop=False
  def run(self):
    while not self.stop:
      print "a"
      time.sleep(10)
t1=printa()
t2=getb(t1)
t1.start()
t2.start()

