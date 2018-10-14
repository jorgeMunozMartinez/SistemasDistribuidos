#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobotsAux.ice')
import drobots
import drobotsAux
import math
import random  

class controllerAtacanteI(drobotsAux.controllerAtacante):
	def __init__(self):
		self.turno=0
		self.robot = None
		self.location = 0
		self.minas=None
		self.robotsAmigos=None
		self.nombre=None
		self.anguloEnemigos=[]
	
	def setRobot(self,robot,minas,robotsAmigos,nombre, current = None):
		self.robot = robot
		self.minas=minas
		self.robotsAmigos=robotsAmigos
		self.nombre=nombre

	def turn(self,current=None):
		self.location=self.robot.location()
		print("ATACANTE-->Turno del robot atacante: "+str(self.nombre))
		print("		Turno número: "+str(self.turno))
		self.minasEnRuta()
		if(self.turno%2==0):
			self.disparar()
		else:
			self.moverRobot()
		print("ATACANTE-->Fin del turno")
		self.turno+=1
		self.anguloEnemigos=[]
		print()

	def minasEnRuta(self, current = None):
		print("ATACANTE-->***Comprobando minas en ruta***")
		salida=False
		listMinas=list(self.minas.list2().values())
		for j in range(0, len(listMinas)):			
			if(listMinas[j].x + 4  == self.location.x or listMinas[j].y + 4 == self.location.y):
				if(listMinas[j].x - 4 == self.location.x or listMinas[j].y - 4 == self.location.y):
					print("	ATACANTE-->Encontrada mina en ruta")	
					print("	ATACANTE-->***Robot atacante moviendose por mina***")
					self.moverRobot()
					salida=True	
		if(salida==False):
			print("	ATACANTE-->No hay minas en ruta")
		print("ATACANTE-->***Fin comprobación minas en ruta***")

	def obtenerEnemigos(self,x,y,current=None):
		anguloB=self.calculoAngulo(x,y,self.robot.location().x,self.robot.location().y)
		if anguloB not in self.anguloEnemigos:
			print("	ATACANTE-->Posicion robot añadida: ("+str(x)+", "+str(y)+")")
			self.anguloEnemigos.append(anguloB)

	def comprobarDetectores(self, current=None):
		print("ATACANTE-->***Comprobando detectores***")
		amigos=list(self.robotsAmigos.list().keys())
		proxisAmigos=list(self.robotsAmigos.list().values())
		index=0
		for keys in amigos:
			if("Detector") in keys and str(self.nombre) in keys:
				detector = drobotsAux.controllerDetectorPrx.uncheckedCast(proxisAmigos[index])
				if detector.detectado()==1:
					angulo=self.calculoAngulo(detector.getPosX(),detector.getPosY(),self.location.x,self.location.y)
					if angulo not in self.anguloEnemigos:
						print("	ATACANTE-->Posicion robot añadida: ("+str(detector.getPosX())+", "+str(detector.getPosY())+")")
						self.anguloEnemigos.append(angulo)
			index+=1
		print("ATACANTE-->***Fin comprobando detectores***")

	def disparar(self, current = None):
		self.comprobarDetectores()
		if(len(self.anguloEnemigos)!=0):
			print("ATACANTE-->***DISPARANDO***")
			try:
				distancia = random.randint(1,10)*random.randint(50,100)
				self.robot.cannon(random.choice(self.anguloEnemigos), distancia)
				print("	ATACANTE-->Distancia recorrida por el misil: "+str(distancia))
			except drobots.NoEnoughEnergy:
				print("ATACANTE-->No hay fuel suficiente para disparar")	
			print("ATACANTE-->***Fin disparo***")
		else:
			print("ATACANTE-->No se han detectado enemigos que disparar")
		
	def moverRobot(self, current = None):
		print("ATACANTE-->***Robot atacante moviendose***")
		try:
			print("	ATACANTE-->Poscion actual :["+str(self.location.x)+", "+str(self.location.y)+"]")
			if(self.location.x > 390):
				self.robot.drive(random.randint(50,350),100)
			elif(self.location.y>390):
				self.robot.drive(random.randint(50,350),100)
			elif(self.location.x < 10):
				self.robot.drive(random.randint(50,350),100)
			elif(self.location.y < 10):
				self.robot.drive(random.randint(50,350),100)
			print("	ATACANTE-->Destino :["+str(self.location.x)+", "+str(self.location.y)+"]")
		except drobots.NoEnoughEnergy:
			print("ATACANTE-->No hay fuel suficiente para moverse")
		print("ATACANTE-->***Fin movimiento del robot***")	

	def calculoPosicion(self, pos ,angulo, current=None):
		return int(abs(pos + math.cos(angulo) * random.randint(1,4)*100))

	def calculoAngulo(self,x,y,locationX,locationY, current=None):
		angulo=math.degrees(math.atan2(x-locationX,y-locationY))
		if angulo<0:
			angulo+=360
		elif angulo>360:
			angulo-=360
		return int(angulo)

	def getMiPosX(self, current=None):
		return self.robot.location().x

	def getMiPosY(self,current=None):
		return self.robot.location().y

	def robotDestroyed(self, current = None):
		print("************************")
		print("Robot atacante destruido")
		print("************************")
		print()
