from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

myapp = Flask(__name__)
myapp.config.from_object('config')
mydb = SQLAlchemy(myapp)

from project.views.users import users_blueprint
from project.views.cases import cases_blueprint
from project.views.students import students_blueprint
from project.views.staffs import staffs_blueprint
from project.views.applications import applications_blueprint

# register our blueprints
myapp.register_blueprint(users_blueprint)
myapp.register_blueprint(cases_blueprint)
myapp.register_blueprint(students_blueprint)
myapp.register_blueprint(staffs_blueprint)
myapp.register_blueprint(staffs_blueprint)
myapp.register_blueprint(applications_blueprint)
