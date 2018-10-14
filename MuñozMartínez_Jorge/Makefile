#!/usr/bin/make -f
# -*- mode:makefile -*-

carpetas: 
	mkdir -p db
	mkdir -p db/node1
	mkdir -p db/node2
	mkdir -p db/node3
	mkdir -p db/node4
	mkdir -p db/node5
	mkdir -p db/registry

nodo1:
	icegridnode --Ice.Config=node1.config

nodo2:
	icegridnode --Ice.Config=node2.config

nodo3:
	icegridnode --Ice.Config=node3.config

nodo4:
	icegridnode --Ice.Config=node4.config

nodo5:
	icegridnode --Ice.Config=node5.config

nodos:
	icegridnode --Ice.Config=node1.config &
	while ! netstat -lptn 2> /dev/null | grep ":4061"; do sleep 1; done
	icegridnode --Ice.Config=node2.config &
	icegridnode --Ice.Config=node3.config &
	icegridnode --Ice.Config=node4.config &
	icegridnode --Ice.Config=node5.config &

ice:
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "application add 'robots.xml'" &
	icegridadmin --Ice.Config=locator.config -u user -p pass -e "application update 'robots.xml'"

all:
	make carpetas
	make nodos
	make ice

clean:
	$(RM) *~
	$(RM) *.pyc
	sudo rm -r db/
	sudo rm -r __pycache__/
	sudo killall icegridnode
	sudo killall -q -9 python

