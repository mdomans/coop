import pyev
import greenlet
import time
from handlers import SIGINTHandler
from events import Event


def dispatch(watcher, events):
    print('switching')
    current = greenlet.getcurrent()
    current.switch()

class Reactor(object):
    
    def __init__(self):
        self._loop = pyev.default_loop()
        self._queue = []
        
    def run(self):
        #create dispatch event
        #create CTRL-C handler
        sigint_handler = SIGINTHandler()
        sigint_handler.install(self)
        dispatch_event = Event(0,2,dispatch)
        dispatch_event.install(self)
        #run loop
        self._loop.loop()

    def add(self, function):
        self._queue.append(greenlet.greenlet(function))
        
