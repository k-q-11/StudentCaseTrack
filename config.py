import os
from werkzeug import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = "\x1b\x0bP\xd6\xe6q\x9e\xfe&1\xbd\x9e\xf6\t\xefO\x90\xc14#\xaf\x89\xbcs"

#SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'mydb.db')
#postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
#SQLALCHEMY_DATABASE_URI = "postgresql://yourusername:yourpassword@localhost:port/yournewdb"
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:s122678@localhost:5433/scts"
ALLOWED_EXTENSIONS = set(['pdf'])
#set the file upload limit to 16 megabytes
#MAX_CONTENT_LENGTH = 16 * 1024 * 1024 	

