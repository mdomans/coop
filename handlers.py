import pyev
import signal

class Handler(object):
    sig = None
    
    def install(self, reactor):
        raise NotImplementedError

def handle_exit(watcher, events):
    print("got SIGINT")

class SIGINTHandler(Handler):
    sig = signal.SIGINT
    
    def __init__(self, *args, **kwargs):
        self.watchers= list(args)
        self.cb = kwargs.get('callback', handle_exit)
        self._signal = None
        
    def _call(self, watcher, events):
        self.cb(watcher, events)
        for w in watcher.data:
            w.stop()
        self._signal.stop()
        watcher.loop.unloop()
        
    def install(self, reactor):
        #signal = pyev.Signal(handlers.SIGINTHandler.sig, self._loop, handlers.handle_exit)
        self._signal = pyev.Signal(self.sig, reactor._loop, self._call)
        self._signal.data = self.watchers
        self._signal.start()
        
    
