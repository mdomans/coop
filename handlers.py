import pyev
import signal

class Handler(object):
    sig = None
    
    def install(self, reactor):
        raise NotImplementedError

class SIGINTHandler(Handler):
    sig = signal.SIGINT
    
    def __init__(self, callback):
        self.cb = callback
        
    def install(self, reactor):
        self._signal = pyev.Signal(self.sig, reactor._loop, self.cb)
        self._signal.start()