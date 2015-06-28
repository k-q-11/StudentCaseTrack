from project import myapp, mydb
from collections import namedtuple
from functools import partial
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, Permission, RoleNeed, UserNeed

project_coordinator_role = RoleNeed('Project Coordinator')
project_coordinator_permission = Permission(project_coordinator_role)

@identity_loaded.connect_via(myapp)
def on_identity_loaded(sender, identity):
	identity.user = current_user
	if hasattr(current_user, 'staff_id'):
		for staff_title in current_user.title_list:
			#print 'staff_title.title: %s' %staff_title.title
			identity.provides.add(RoleNeed(staff_title.title))

