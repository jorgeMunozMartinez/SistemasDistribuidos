#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobotsAux.ice')
import drobots
import drobotsAux
import math
import random

class controllerDefensorI(drobotsAux.controllerDefensor):
	def __init__(self):
		self.turno=0
		self.robot = None
		self.location = 0
		self.angulosAmigos = []
		self.minas=None
		self.robotsAmigos=None
		self.nombre=None
	
	def setRobot(self,robot,minas,robotsAmigos,nombre, current = None):
		self.robot = robot
		self.minas=minas
		self.robotsAmigos=robotsAmigos
		self.nombre=nombre

	def turn(self,current=None):
		self.angulosAmigos=[]
		self.location=self.robot.location()
		print("DEFENSOR-->Turno del robot defensor: "+str(self.nombre))
		print("		Turno número: "+str(self.turno))
		self.minasEnRuta()
		self.escanear()
		self.moverRobot()
		print("DEFENSOR-->Fin del turno")
		self.turno+=1
		print()

	def minasEnRuta(self, current = None):
		print("DEFENSOR-->***Comprobando minas en ruta***")
		listMinas=list(self.minas.list2().values())
		salida=False
		for j in range(0, len(listMinas)):	
			if(listMinas[j].x + 4  == self.location.x or listMinas[j].y + 4 == self.location.y):
				if(listMinas[j].x - 4 == self.location.x or listMinas[j].y - 4 == self.location.y):
					print("	DEFENSOR-->Encontrada mina en ruta")
					print("	DEFENSOR-->***Robot defensor moviendose por mina***")
					self.moverRobot(self.location)	
					salida=True					
		if(salida==False):
			print("	DEFENSOR-->No hay minas en ruta")
		print("DEFENSOR-->***Fin comprobación minas en ruta***")

	def moverRobot(self, current = None):
		print("DEFENSOR-->***Robot defensor moviendose***")
		try:
			print("	DEFENSOR-->Poscion actual :["+str(self.location.x)+", "+str(self.location.y)+"]")
			if(self.location.x > 390):
				conducir=self.calculoAngulo(random.randint(50,350),random.randint(50,350),self.location.x,self.location.y)
				self.robot.drive(conducir,100)
			elif(self.location.y>390):
				conducir=self.calculoAngulo(random.randint(50,350),random.randint(50,350),self.location.x,self.location.y)
				self.robot.drive(conducir,100)
			elif(self.location.x < 10):
				conducir=self.calculoAngulo(random.randint(50,350),random.randint(50,350),self.location.x,self.location.y)
				self.robot.drive(conducir,100)
			elif(self.location.y < 10):
				conducir=self.calculoAngulo(random.randint(50,350),random.randint(50,350),self.location.x,self.location.y)
				self.robot.drive(conducir,100)
			print("	DEFENSOR-->Destino :["+str(self.location.x)+", "+str(self.location.y)+"]")
		except drobots.NoEnoughEnergy:
			print("DEFENSOR-->No hay fuel suficiente para moverse")	
		print("DEFENSOR-->***Fin movimiento del robot***")			

	def escanear(self, current = None):
		angulo=random.randint(0, 359)
		amplitud=20
		self.getPosAmigos()
		print("DEFENSOR-->***Realizando escaneo***")
		print("	DEFENSOR-->Grados de escaneo: "+str(angulo))
		try:
			robotsEncontrados = self.robot.scan(angulo, amplitud)
			if(robotsEncontrados > 0):
				print("	DEFENSOR-->Se han encontrado: "+str(robotsEncontrados)+" robots")
				if(((angulo +10) not in self.angulosAmigos)or((angulo -10) not in self.angulosAmigos)):
					print("	DEFENSOR-->Enemigo Encontrado")
					amigos=list(self.robotsAmigos.list().keys())
					proxisAmigos=list(self.robotsAmigos.list().values())
					x=self.calculoPosicion(self.location.x,angulo)
					y=self.calculoPosicion(self.location.y,angulo)
					index=0
					print("		Enemigo encontrado, enviando posiciones")		
					for keys in amigos:
						if("Atacante") in keys and str(self.nombre) in keys:
							atacante = drobotsAux.controllerAtacantePrx.uncheckedCast(proxisAmigos[index])
							atacante.obtenerEnemigos(x,y)
						elif("Completo") in keys and str(self.nombre) in keys:
							completo = drobotsAux.controllerCompletoPrx.uncheckedCast(proxisAmigos[index])
							completo.obtenerEnemigos(x,y)
						index+=1
				else:
					print("	DEFENSOR-->Amigo Encontrado")
			else:
				print("	DEFENSOR-->No se han encontrado robots")
		except drobots.NoEnoughEnergy:
			print("DEFENSOR-->No hay fuel suficiente para escanear el terreno")
		print("DEFENSOR-->***Fin del escaneo***")	

	def getPosAmigos(self, current = None):
		amigos=list(self.robotsAmigos.list().keys())
		proxisAmigos=list(self.robotsAmigos.list().values())
		index=0
		for keys in amigos:
			if("Atacante") in keys and str(self.nombre) in keys:
				atacante = drobotsAux.controllerAtacantePrx.uncheckedCast(proxisAmigos[index])
				self.angulosAmigos.append(self.calculoAngulo(atacante.getMiPosX(),atacante.getMiPosY(),self.location.x,self.location.y))
			elif("Defensor") in keys and str(self.nombre) in keys:
				defensor = drobotsAux.controllerDefensorPrx.uncheckedCast(proxisAmigos[index])
				self.angulosAmigos.append(self.calculoAngulo(defensor.getMiPosX(),defensor.getMiPosY(),self.location.x,self.location.y))
			elif("Completo") in keys and str(self.nombre) in keys:
				completo = drobotsAux.controllerCompletoPrx.uncheckedCast(proxisAmigos[index])
				self.angulosAmigos.append(self.calculoAngulo(completo.getMiPosX(),completo.getMiPosY(),self.location.x,self.location.y))
			index+=1

	def calculoAngulo(self,x,y,locationX,locationY, current=None):
		angulo=math.degrees(math.atan2(x-locationX,y-locationY))
		if angulo<0:
			angulo+=360
		elif angulo>360:
			angulo-=360
		return int(angulo)
		
	def calculoPosicion(self, pos ,angulo, current=None):
		return int(abs(pos + math.cos(angulo) * random.randint(1,4)*100))

	def getMiPosX(self, current=None):
		return self.robot.location().x

	def getMiPosY(self,current=None):
		return self.robot.location().y
	def robotDestroyed(self, current = None):
		print("************************")
		print("Robot defensor destruido")
		print("************************")
		print()
