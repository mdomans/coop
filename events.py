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
        self._cb = callback
        self.events = events
        
    def install(self, reactor):
        self._io = pyev.Io(self.fd, self.events, reactor._loop, self._cb, 0)
        self._io.start()
        
    def _call(self, watcher, data):
        if self._cb: self._cb(watcher, data)
        self._io.stop()
        
class ReadEvent(FDEvent):
    def __init__(self, fd, callback=None):
        FDEvent.__init__(self, fd, pyev.EV_READ, callback)
        
class WriteEvent(FDEvent):
    def __init__(self, fd, callback):
        FDEvent, self.__init__(self, fd, pyev.EV_WRITE, callback)
        
        
    
