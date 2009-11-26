import greenlet

class Semaphore(object):

    def __init__(self, value):
        self._inner = value
        self._waiters = list()

    @property
    def is_blocked(self):
        return self._inner<0
            
    def acquire(self):
        if not self.is_blocked:
            self._inner-=1
        else:
            g = greenlet.getcurrent()# our greenlet
            self._waiters.append(g)
            g.parent.switch()
        
    def release(self):
        self._inner+=1
        if self._inner>0:
            g = self._waiters.pop(0)
            g.switch()        
    
class Pool(object):
    def __init__(self, size):
        self._queue = []
        self._bound = size
        self._tasks = []

    @property
    def _running(self):
        return len(self._queue)>0 or len(self._tasks)>0
    
        
    def add(self, function):
        self._queue.append(greenlet.greenlet(function))
        
    def run(self):
        while self._running:
            if len(self._tasks)<self._bound and len(self._queue):
                task = self._queue.pop(0)
            else:
                task = self._tasks.pop(0)
            task.switch()
            if not task.dead:
                self._tasks.append(task)
            
            