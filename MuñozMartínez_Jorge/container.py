#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobotsAux.ice')
import drobotsAux

class ContainerI(drobotsAux.controllerContainer):
    def __init__(self):
        self.proxies = dict()
        
    def link(self, key, proxy, current=None):
        if(key) in self.proxies:
            raise drobotsAux.AlreadyExists(key)
        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def link2(self, key, proxy, current=None):
        if(key) in self.proxies:
            raise drobotsAux.AlreadyExists(key)
        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        if not (key) in self.proxies:
            raise drobotsAux.NoSuchKey(key)
        print("unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies

    def list2(self, current=None):
        return self.proxies

    def pruebaEntrada(self, current=None):
        print("Saludos")

class Server(Ice.Application):
    def run(self,argv): 
        broker = self.communicator()
        adaptador = broker.createObjectAdapter("ContainerAdapter")
        print()
        containerController=ContainerI()
        containerMinas=ContainerI()
        containerFacotrias=ContainerI()
        proxyContainer = adaptador.add(containerController,broker.stringToIdentity("containerControlador"))
        proxyMinas = adaptador.add(containerMinas,broker.stringToIdentity("containerMinas"))
        proxyFactoria = adaptador.add(containerFacotrias,broker.stringToIdentity("containerFactory"))
        adaptador.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
if __name__ == '__main__':
    sys.exit(Server().main(sys.argv))   
