#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
import os
Ice.loadSlice('--all drobotsAux.ice')
import drobotsAux
from controllerAtacante import controllerAtacanteI
from controllerDefensor import controllerDefensorI
from controllerCompleto import controllerCompletoI
from controllerDetector import controllerDetectorI

class factoriaI(drobotsAux.controllerFactory):

	def make(self,robot ,tipo ,minas,controllerAmigos,nombre, current=None):
		print("FACTORÍA")
		if(tipo == "atacante"):
			proxyController = current.adapter.addWithUUID(controllerAtacanteI())
			controller = drobotsAux.controllerAtacantePrx.uncheckedCast(current.adapter.createDirectProxy(proxyController.ice_getIdentity()))	
			controller.setRobot(robot,minas,controllerAmigos,nombre)
			print("FACTORÍA--> creado robot atacante: "+str(controller))
		if(tipo == "defensor"):
			proxyController = current.adapter.addWithUUID(controllerDefensorI())
			controller = drobotsAux.controllerDefensorPrx.uncheckedCast(current.adapter.createDirectProxy(proxyController.ice_getIdentity()))	
			controller.setRobot(robot,minas,controllerAmigos,nombre)
			print("FACTORÍA--> creado robot defensor: "+str(controller))
		if(tipo == "completo"):
			proxyController = current.adapter.addWithUUID(controllerCompletoI())
			controller = drobotsAux.controllerCompletoPrx.uncheckedCast(current.adapter.createDirectProxy(proxyController.ice_getIdentity()))
			controller.setRobot(robot,minas,controllerAmigos,nombre)
			print("FACTORÍA--> creado robot completo: "+str(controller))
		return controller

	def makeDetector(self,current=None):
		print("FACTORÍA")
		proxyController = current.adapter.addWithUUID(controllerDetectorI())
		controller = drobotsAux.controllerDetectorPrx.uncheckedCast(current.adapter.createDirectProxy(proxyController.ice_getIdentity()))	
		print("FACTORÍA--> creado robot detector: "+str(controller))
		return controller

class Server(Ice.Application):
	def run(self,args):
		adapter = self.communicator().createObjectAdapter("FactoryAdapter")
		#print("Adapter F :"+str(adapter))
		proxy =adapter.add(factoriaI(),self.communicator().stringToIdentity("factoria"))
		containerFactory = drobotsAux.controllerContainerPrx.uncheckedCast(self.communicator().stringToProxy("containerFactory"))
		#containerFactory.pruebaEntrada()
		containerFactory.link(str(os.getpid()),proxy)
		adapter.activate()
		self.shutdownOnInterrupt()
		self.communicator().waitForShutdown()

if __name__ == '__main__':
	sys.exit(Server().main(sys.argv))	
