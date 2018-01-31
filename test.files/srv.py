#!/usr/bin/python
import Pyro4
import Pyro4.naming
import thread
import socket

@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        return "Hello, {0}. Here is your fortune message:\n" \
               "Tomorrow's lucky number is 12345678.".format(name)


def start():
    hostname=socket.gethostname()
    #Pyro4.naming.startNSloop(host=hostname, port=9099, hmac="skot")
    Pyro4.naming.startNSloop(hmac="skot")

thread.start_new_thread(start,())

#daemon = Pyro4.Daemon(host=socket.gethostname(), port=9090)
daemon = Pyro4.Daemon()
daemon._pyroHmacKey = "skot"
#ns = Pyro4.locateNS(host=socket.gethostname(), port=9099,hmac_key="skot") 
ns = Pyro4.locateNS(hmac_key="skot") 
uri = daemon.register(GreetingMaker())
ns.register("myserver.test", uri)

daemon.requestLoop()