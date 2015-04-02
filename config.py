import os
basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = "you will never get this"
#SQLALCHEMY_DATABASE_URI = 'sqlite:///mydb.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'mydb.db')