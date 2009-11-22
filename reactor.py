import pyev
import greenlet
import time
from handlers import SIGINTHandler
from events import Event

class Reactor(object):
    
    def __init__(self):
        self._current = greenlet.getcurrent()
        self._loop = pyev.default_loop()
        self._queue = []
        
    def run(self):
        #create dispatch event
        Event(0, 2, self.dispatch).install(self)
        #create CTRL-C handler
        SIGINTHandler(self.handle_exit).install(self)
        #run loop
        self._loop.loop()
        
    def dispatch(self, watcher, events):
        print('switching')
        current = self._queue.pop(0)
        current.switch()
        self._queue.append(current)
        
    def add(self, function):
        self._queue.append(greenlet.greenlet(function))
        

    def handle_exit(self, watcher, events):
        print("got SIGINT")
        # optional - stop all watchers
        if watcher.data:
            print("stopping watchers: {0}".format(watcher.data))
            for w in watcher.data:
                w.stop()
        # unloop all nested loop
        print("stopping the loop: {0}".format(watcher.loop))
        watcher.loop.unloop()