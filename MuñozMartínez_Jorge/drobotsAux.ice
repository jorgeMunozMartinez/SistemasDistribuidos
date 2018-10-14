// -*- mode:c++ -*-
#include "drobots.ice"

module drobotsAux {

	exception AlreadyExists { string key; };
	exception NoSuchKey { string key; };

	dictionary<string, Object*> ObjectPrxDict;
	dictionary<string, drobots::Point> PointPrxDict;

	interface controllerContainer {
		void link(string key,Object* proxy) throws AlreadyExists;
		void link2(string key,drobots::Point point) throws AlreadyExists;
		void unlink(string key) throws NoSuchKey;
		ObjectPrxDict list();
		PointPrxDict list2();
		void pruebaEntrada();
	};

	interface controllerFactory{
		drobots::RobotController* make(drobots::Robot* bot, string tipo,controllerContainer* minas,controllerContainer* containerController,string nombre);
		drobots::DetectorController* makeDetector();
	};

	interface controllerAtacante extends drobots::RobotController {
		void setRobot(drobots::Robot* robot,controllerContainer* minas,controllerContainer* amigos,string nombre);
		void obtenerEnemigos(int x, int y);
		int getMiPosX();
		int getMiPosY();
		};

	interface controllerDefensor extends drobots::RobotController {
		void setRobot(drobots::Robot* robot,controllerContainer* minas,controllerContainer* amigos, string nombre);
		int getMiPosX();
		int getMiPosY();
		};

	interface controllerCompleto extends drobots::RobotController {
		void setRobot(drobots::Robot* robot,controllerContainer* minas,controllerContainer* amigos, string nombre);
		int getMiPosX();
		int getMiPosY();
		void obtenerEnemigos(int x, int y);
		};

	interface controllerDetector extends drobots::DetectorController {
		int getPosX();
		int getPosY();
		int detectado();
		};


 };