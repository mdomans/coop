import pyev
import greenlet
import signal
import time

class Reactor(object):
    
    def __init__(self):
        self._reads = {}
        self._writes = {}
        self._queue = []
        self._current = greenlet.getcurrent()
        self._loop = pyev.default_loop()
        
    def run(self):
        # initialise and start a repeating timer
        timer = pyev.Timer(0, 2, self._loop, self.dispatch, 0)
        timer.start()
        # initialise and start a Signal watcher
        sig = pyev.Signal(signal.SIGINT, self._loop, self.handle_exit)
        sig.data = [timer, sig] # optional
        sig.start()
        # now wait for events to arrive
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

def main():
    reactor = Reactor()
    def print1():
        counter=10
        while counter:
            print 1
            counter-=1
            time.sleep(10)
    
    def print2():
        print 2
        

    reactor.add(print1)
    reactor.add(print2)
    
    reactor.run()
        

if __name__ == "__main__":
    main()