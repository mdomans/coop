import pyev
import greenlet
import time
from handlers import SIGINTHandler
from events import IntervalEvent


class Reactor(object):
    
    def __init__(self):
        self._loop = pyev.default_loop()
        self._current = greenlet.getcurrent()
        self._queue = []
        self._handlers = []
        self._events = []
        
    def run(self):
        #create dispatch event
        #create CTRL-C handler
        sigint_handler = SIGINTHandler()
        self.install(sigint_handler)
        dispatch_event = IntervalEvent(2,self.dispatch)
        self.install(dispatch_event)
        #run loop
        self._loop.loop()

    def dispatch(self, watcher, events, data=None):
        print('switching')
        current = self._queue.pop(0)
        current.switch()
        self._queue.append(current)

    def add(self, function):
        self._queue.append(greenlet.greenlet(function))
        
    def install(self, handler):
        handler.install(self)
        
    def install_handler(self, handler):
        self._handlers.append(handler)
        handler.install(self)