import pyev
import signal

class Handler(object):
    sig = None
    
    def install(self, reactor):
        raise NotImplementedError

def handle_exit(watcher, events):
    print("got SIGINT")
    # optional - stop all watchers
    if watcher.data:
        print("stopping watchers: {0}".format(watcher.data))
        for w in watcher.data:
            w.stop()
    # unloop all nested loop
    print("stopping the loop: {0}".format(watcher.loop))
    watcher.loop.unloop()

class SIGINTHandler(Handler):
    sig = signal.SIGINT
    
    def __init__(self, callback=handle_exit):
        self.cb = callback
        self._signal = None
        
    def install(self, reactor):
        #signal = pyev.Signal(handlers.SIGINTHandler.sig, self._loop, handlers.handle_exit)
        self._signal = pyev.Signal(self.sig, reactor._loop, handle_exit)
        self._signal.start()
        
    
