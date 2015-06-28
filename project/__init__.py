from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.principal import Principal

myapp = Flask(__name__)
bcrypt = Bcrypt(myapp)
mylogin_manager = LoginManager()
mylogin_manager.session_protection = 'strong'
mylogin_manager.init_app(myapp)
myprincipals = Principal(myapp)
myapp.config.from_object('config')
mydb = SQLAlchemy(myapp)

from project.views.students import students_blueprint
from project.views.staffs import staffs_blueprint
from project.views.applications import applications_blueprint
#from project.views.projectcases import projectcases_blueprint
from project.views.cases import cases_blueprint

# register our blueprints
myapp.register_blueprint(students_blueprint)
myapp.register_blueprint(staffs_blueprint)
myapp.register_blueprint(applications_blueprint)
#myapp.register_blueprint(projectcases_blueprint)
myapp.register_blueprint(cases_blueprint)

'''
from project.models import Staff
mylogin_manager.login_view = "staffs.login" # sets end point for login page

@mylogin_manager.user_loader
def load_user(user_id):
	if user_id.isdigit():
		return Stduent.query.filter(Student.study_no == int(user_id)).first()
	else:
		return Staff.query.filter(Staff.staff_id == user_id).first()
'''		