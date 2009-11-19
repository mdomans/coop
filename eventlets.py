urls = ["http://www.google.com/intl/en_ALL/images/logo.gif",
       "http://wiki.secondlife.com/w/images/secondlife.jpg",
       "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"]

import time
from eventlet import coros

# this imports a special version of the urllib2 module that uses non-blocking IO
from eventlet.green import urllib2
from urllib2 import urlopen

def fetch(url):
    print "%s fetching %s" % (time.asctime(), url)
    data = urllib2.urlopen(url)
    print "%s fetched %s" % (time.asctime(), data)

pool = coros.CoroutinePool(max_size=4)
waiters = []
print time.asctime()
for url in urls:
    waiters.append(pool.execute(fetch, url))

# wait for all the coroutines to come back before exiting the process
for waiter in waiters:
    waiter.wait()
print time.asctime()

print time.asctime()
for url in urls:
    print "%s fetching %s" % (time.asctime(), url)
    data = urlopen(url)
    print "%s fetched %s" % (time.asctime(), data)
print time.asctime()
