import pyev

class TimeEvent(object):
    
    def __init__(self, after=0, interval=0, callback=None):
        self.after = after
        self.interval = interval
        self.callback = callback
        
    def install(self, reactor):
        self._timer = pyev.Timer(self.after, self.interval, reactor._loop, self.callback, 0)
        self._timer.start()
        

class IntervalEvent(TimeEvent):
    def __init__(self, interval, callback):
        self.after = interval
        self.interval = interval
        self.callback = callback
            
            
class FDEvent(object):
    def __init__(self, fd, events, callback):
        self.fd = fd
        self.callback = callback
        self.events = events
        
    def install(self, reactor):
        self._io = pyev.Io(self.fd, self.events, reactor._loop, self.callback, 0)
        self._io.start()
        
class ReadEvent(FDEvent):
    def __init__(self, fd, callback):
        super(FDEvent, self).__init__(self, fd, pyev.EV_READ, callback)
        
        
class WriteEvent(FDEvent):
    def __init__(self, fd, callback):
        super(FDEvent, self).__init__(self, fd, pyev.EV_WRITE, callback)