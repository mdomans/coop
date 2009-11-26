from reactor import Reactor
import events
import handlers
import socket
import greenlet
import os, signal
from nose.tools import assert_true

def test_io_watcher():

    reactor = Reactor()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost',8001))
    def cb(a,b):
        # should be reworked, this is a bit of a hammer
        os.kill(os.getpid(), signal.SIGINT)
    io_event = events.ReadEvent(s, cb)
    reactor.install(io_event)
    reactor.run()