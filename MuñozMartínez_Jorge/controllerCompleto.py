#!/usr/bin/python3
#-*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobotsAux.ice')
import drobotsAux
import drobots
import math
import random

class controllerCompletoI(drobotsAux.controllerCompleto):
	def __init__(self):
		self.turno=0
		self.robot = None
		self.location = 0
		self.angulosAmigos = []
		self.anguloEnemigos = []
		self.minas=None
		self.robotsAmigos=None
		self.nombre=None
	
	def setRobot(self,robot,minas,robotsAmigos,nombre, current = None):
		self.robot = robot
		self.minas=minas
		self.robotsAmigos=robotsAmigos
		self.nombre=nombre

	def turn(self, current=None):
		self.angulosAmigos=[]
		self.location=self.robot.location()
		print("COMPLETO-->Turno del robot completo: "+str(self.nombre))
		print("		Turno número: "+str(self.turno))
		self.minasEnRuta()
		self.escanear()
		if(self.turno%2==0):
			self.disparar()
		else:
			self.moverRobot()
		print("COMPLETO-->Fin del turno")
		self.turno+=1
		self.anguloEnemigos=[]
		print()

	def minasEnRuta(self, current = None):
		print("COMPLETO-->***Comprobando minas en ruta***")
		listMinas=list(self.minas.list2().values())
		salida=False
		for j in range(0, len(listMinas)):
			if(listMinas[j].x + 4  == self.location.x or listMinas[j].y + 4 == self.location.y):
				if(listMinas[j].x - 4 == self.location.x or listMinas[j].y - 4 == self.location.y):
					print("	COMPLETO-->Encontrada mina en ruta")
					print("	COMPLETO-->***Robot defensor moviendose por mina***")
					self.moverRobot()	
					salida=True					
		if(salida==False):
			print("	COMPLETO-->No hay minas en ruta")
		print("COMPLETO-->***Fin comprobación minas en ruta***")

	def obtenerEnemigos(self,x,y,current=None):
		anguloB=self.calculoAngulo(x,y,self.robot.location().x,self.robot.location().y)
		if anguloB not in self.anguloEnemigos:
			print("	COMPLETO-->Posicion robot añadida: ("+str(x)+", "+str(y)+")")
			self.anguloEnemigos.append(anguloB)

	def comprobarDetectores(self, current=None):
		print("COMPLETO-->***Comprobando detectores***")
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
		print("COMPLETO-->***Fin comprobando detectores***")

	def disparar(self, current = None):
		self.comprobarDetectores()
		if(len(self.anguloEnemigos)!=0):
			print("COMPLETO-->***DISPARANDO***")
			try:
				distancia = random.randint(1,10)*random.randint(50,100)
				self.robot.cannon(random.choice(self.anguloEnemigos), distancia)
				print("	COMPLETO-->Distancia recorrida por el misil: "+str(distancia))
			except drobots.NoEnoughEnergy:
				print("	COMPLETO-->No hay fuel suficiente para disparar")
			print("COMPLETO-->***Fin disparo***")
		else:
			print("COMPLETO-->No se han detectado enemigos que disparar")

	def moverRobot(self, current = None):
		print("COMPLETO-->***Robot defensor moviendose***")
		try:
			print("	COMPLETO-->Poscion actual :["+str(self.location.x)+", "+str(self.location.y)+"]")
			if(self.location.x > 390):
				self.robot.drive(random.randint(50,200),100)
			elif(self.location.y>390):
				self.robot.drive(random.randint(50,200),100)
			elif(self.location.x < 10):
				self.robot.drive(random.randint(200,350),100)
			elif(self.location.y < 10):
				self.robot.drive(random.randint(200,350),100)
			print("	COMPLETO-->Destino :["+str(self.location.x)+", "+str(self.location.y)+"]")
		except drobots.NoEnoughEnergy:
			print("	COMPLETO-->No hay fuel suficiente para moverse")	
		print("COMPLETO-->***Fin movimiento del robot***")
		
	def escanear(self, current = None):
		angulo=random.randint(10, 349)
		amplitud=20
		self.getPosAmigos()
		print("COMPLETO-->***Realizando escaneo***")
		print("	COMPLETO-->Grados de escaneo: "+str(angulo))
		try:
			robotsEncontrados = self.robot.scan(angulo, amplitud)
			if(robotsEncontrados > 0):
				print("	COMPLETO-->Se han encontrado: "+str(robotsEncontrados)+" robots")
				if(((angulo +10) not in self.angulosAmigos)or((angulo -10) not in self.angulosAmigos)):
					print("	COMPLETO-->Enemigo Encontrado")
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
					print("	COMPLETO-->Amigo Encontrado")
			else:
				print("	COMPLETO-->No se han encontrado robots")
		except drobots.NoEnoughEnergy:
			print("COMPLETO-->No hay fuel suficiente para escanear el terreno")
		print("COMPLETO-->***Fin del escaneo***")	

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

	def getMiPosX(self, current=None):
		return self.robot.location().x

	def getMiPosY(self,current=None):
		return self.robot.location().y

	def calculoAngulo(self,x,y,locationX,locationY, current=None):
		angulo=math.degrees(math.atan2(x-locationX,y-locationY))
		if angulo<0:
			angulo+=360
		elif angulo>360:
			angulo-=360
		return int(angulo)

	def calculoPosicion(self, pos ,angulo, current=None):
		return int(abs(pos + math.cos(angulo) * random.randint(1,4)*100))

	def robotDestroyed(self, current = None):
		print("************************")
		print("Robot completo destruido")
		print("************************")
		print()