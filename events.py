import pyev

class Event(object):
    
    def __init__(self, after=0, interval=0, callback=None):
        self.after = after
        self.interval = interval
        self.callback = callback
        
    def install(self, reactor):
        self._timer = pyev.Timer(self.after, self.interval, reactor._loop, self.callback, 0)
        self._timer.start()
        

