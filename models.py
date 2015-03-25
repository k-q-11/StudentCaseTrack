from views import mydb
from werkzeug.security import generate_password_hash, check_password_hash

class User(mydb.Model):
	__table__name = 'users'
	# risk overflow
	uid = mydb.Column(mydb.Integer, primary_key=True, autoincrement=True) 
	username = mydb.Column(mydb.String, unique=True, nullable = False)
	email = mydb.Column(mydb.String, unique=True, nullable = False)
	#pwdhash = db.Column(db.String, nullable = False)
	password = mydb.Column(mydb.String, nullable = False)
	

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		#self.set_password(password)
		self.password = password

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def __repr__(self):
		return '<User %r>' % self.username