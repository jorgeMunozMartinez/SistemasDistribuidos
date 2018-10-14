#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobotsAux.ice')
import drobotsAux


class controllerDetectorI(drobotsAux.controllerDetector):
	def __init__(self):
		self.robotsEnemigos = -1
		self.posicion = None

	def alert(self,posicion, robotsEnemigos, current = None):
		self.robotsEnemigos = robotsEnemigos
		self.posicion = posicion
		print("----Warning too much intimidating robot detected----")
		print("DETECTOR--> robot encontrados en la posición: ("+str(self.posicion.x)+", "+str(self.posicion.y)+")")   
		print()

	def robotDestroyed(self, current = None):
		print("************************")
		print("Robot detector destruido")
		print("************************")
		print()

	def detectado(self,current=None):
		if(self.robotsEnemigos>0):
			return 1
		else:
			return 0

	def getPosX(self, current=None):
		if(self.robotsEnemigos>0):
			return self.posicion.x

	def getPosY(self, current=None):
		if(self.robotsEnemigos>0):
			return self.posicion.y

