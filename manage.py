from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os
from project import myapp, mydb
myapp.config.from_object('config')
mymigrate = Migrate(myapp, mydb)
mymanager = Manager(myapp)

mymanager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	mymanager.run()