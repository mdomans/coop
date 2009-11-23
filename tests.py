from reactor import Reactor
import greenlet

def main():
    reactor = Reactor()
    def print1():
        counter=10
        while counter:
            print 1
            counter-=1
    
    def print2():
        print 2
        

    
    reactor.add(print1)
    reactor.add(print2)
    reactor.run()
        

main()