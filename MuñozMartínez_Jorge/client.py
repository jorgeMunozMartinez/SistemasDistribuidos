#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
import random
import math
Ice.loadSlice('--all drobotsAux.ice')
import drobots
import drobotsAux

class PlayerI(drobots.Player):

	def __init__(self,containerFactorias,containerController,containerMinas,name):
		self.detector_controller = None
		self.numeroDetectores=0
		self.numeroFactoria=0 
		self.containerFactorias=containerFactorias
		self.containerController=containerController
		self.containerMinas=containerMinas
		self.name=name
		self.contMin = 0
		self.cont=0
		self.contDetec=0

	def makeController(self, bot, current):
		#3 tipos de controladores de robots, atacante, defensor y completo
		print("JUGADOR 1: "+str(self.name)+"--> creando controlador: "+str(self.cont))
		proxisFactoria=list(self.containerFactorias.list().values())
		if(bot.ice_ids() == ['::Ice::Object', '::drobots::Attacker', '::drobots::RobotBase']): 
			print("JUGADOR 1-->Creando controlador del atacante usando factoría: "+str(proxisFactoria[self.cont]))
			factoria=drobotsAux.controllerFactoryPrx.uncheckedCast(proxisFactoria[self.cont])
			controllerAtacante= factoria.make(bot,"atacante",self.containerMinas,self.containerController,self.name)
			#print("JUGADOR 1-->Creado robot atacante: "+str(controllerAtacante))    
			self.containerController.link(str(self.name)+" Atacante "+str(self.cont),controllerAtacante)   
			self.cont+=1
			print()
			return controllerAtacante
		elif(bot.ice_ids() == ['::Ice::Object', '::drobots::Defender', '::drobots::RobotBase']):
			print("JUGADOR 1-->Creando controlador del defensor usando factoría: "+str(proxisFactoria[self.cont]))
			factoria=drobotsAux.controllerFactoryPrx.uncheckedCast(proxisFactoria[self.cont]) 
			controllerDefensor=factoria.make(bot,"defensor",self.containerMinas,self.containerController,self.name) 
			#print("JUGADOR 1-->Creado robot defensor: "+str(controllerDefensor))
			self.containerController.link(str(self.name)+" Defensor "+str(self.cont),controllerDefensor)
			self.cont+=1
			print()
			return controllerDefensor
		elif(bot.ice_ids() == ['::Ice::Object', '::drobots::Attacker', '::drobots::Defender', '::drobots::Robot', '::drobots::RobotBase']):
			print("JUGADOR 1-->Creando controlador del completo usando factoría: "+str(proxisFactoria[self.cont]))
			factoria=drobotsAux.controllerFactoryPrx.uncheckedCast(proxisFactoria[self.cont]) 
			controllerCompleto=factoria.make(bot,"completo",self.containerMinas,self.containerController,self.name)
			#print("JUGADOR 1-->Creado robot completo: "+str(controllerCompleto)) 
			self.containerController.link(str(self.name)+" Completo "+str(self.cont),controllerCompleto) 
			self.cont+=1
			print()
			return controllerCompleto

	def makeDetectorController(self, current):
		print("JUGADOR 1: "+str(self.name)+"--> creando controlador detector: "+str(self.contDetec))
		proxisFactoria=list(self.containerFactorias.list().values())
		print("JUGADOR 1-->Creando controlador del detector usando factoría: "+str(proxisFactoria[self.contDetec]))
		factoria = drobotsAux.controllerFactoryPrx.uncheckedCast(proxisFactoria[self.contDetec])
		controllerDetector = factoria.makeDetector()
		#print("JUGADOR 1-->Creado robot detector: "+str(controllerDetector)) 
		self.containerController.link(str(self.name)+" Detector "+str(self.contDetec),controllerDetector) 
		self.contDetec+=1
		print()
		return controllerDetector

	def getMinePosition(self, current):
		print("JUGADOR 1: "+str(self.name)+"--> creando mina: "+str(self.contMin))
		mina = drobots.Point(random.randint(0,399), random.randint(0,399))
		self.containerMinas.link2(str(self.name)+" Mina "+str(self.contMin),mina)
		self.contMin += 1
		print()
		return mina

	def win(self, current):
		print("JUGADOR: "+str(self.name))
		print("You win ¯\(^-^)/¯ ")
		current.adapter.getCommunicator().shutdown()

	def lose(self, current):
		print("JUGADOR: "+str(self.name))
		print("You lose ¯\_(ツ)_/¯ ")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current):
		print("The game was aborted")
		current.adapter.getCommunicator().shutdown()


class ClientApp(Ice.Application):

	def run(self, argv):
		broker = self.communicator()
		#
		adapter = broker.createObjectAdapter("PlayerAdapter")

		proxyFactoria = broker.stringToProxy("containerFactory")
		containerFactorias = drobotsAux.controllerContainerPrx.uncheckedCast(proxyFactoria)

		proxyMinas = broker.stringToProxy("containerMinas")
		containerMinas = drobotsAux.controllerContainerPrx.uncheckedCast(proxyMinas)

		proxyContainer = broker.stringToProxy("containerControlador")
		containerController = drobotsAux.controllerContainerPrx.uncheckedCast(proxyContainer)
		#

		# Using "propertyToProxy" forces to define the property "GameProxy"
		#game_prx = drobots.GamePrx.checkedCast(broker.propertyToProxy("GameProxy"))

		proxyGame = broker.propertyToProxy("Factoria")
		gameFactory = drobots.GameFactoryPrx.checkedCast(proxyGame)
		game_prx = gameFactory.makeGame("nombre", 2)

		# Using "getProperty" forces to define the property "PlayerName"
		name = "".join(random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(3))+ str(random.randint(0,9)) 

		servant = PlayerI(containerFactorias,containerController,containerMinas,name)
		player_prx = adapter.addWithUUID(servant)
		directProxyPlayer = adapter.createDirectProxy(player_prx.ice_getIdentity())
		player = drobots.PlayerPrx.uncheckedCast(directProxyPlayer)
		adapter.activate()
		try:
			print("Conectando a la partida {} con nombre de jugador {}".format(game_prx, name))
			game_prx.login(player, name)
		except drobots.InvalidName as e:
			print("Nombre de jugador inválido")
			print(str(e.reason))
		except drobots.GameInProgress:
			print("Partida en curso.")
		except drobots.BadNumberOfPlayers:
			print("Número de jugadores no válido")
		except drobots.InvalidProxy:
			print("Proxy inválido")  
		except Ice.ConnectionRefusedException:
			print()
			print("Error de conexion con factoría jugador: "+str(name))
			print("Conectando con GameProxy")
			print("Conectando a la partida {} con nombre de jugador {}".format(game_prx, name))
			game_prx = drobots.GamePrx.checkedCast(broker.propertyToProxy("GameProxy"))
			game_prx.login(player, name)
		except Exception as ex:
			print("Error ocurrido {}".format(ex))

		self.shutdownOnInterrupt()
		broker.waitForShutdown()

if __name__ == '__main__':
	client = ClientApp()
	retval = client.main(sys.argv)
	sys.exit(retval)