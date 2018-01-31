#!/usr/bin/python
#saved as greeting-client.py
import Pyro4
import Pyro4.naming

#name = raw_input("What is your name? ").strip()

#nameserver = Pyro4.naming.locateNS(host="Apple-TV", port=9099, broadcast=True, hmac_key="skot")
nameserver = Pyro4.naming.locateNS(hmac_key="skot")
uri = nameserver.lookup("myserver.test")
greeting_maker = Pyro4.Proxy(uri)

print(greeting_maker.get_fortune("Ivan"))