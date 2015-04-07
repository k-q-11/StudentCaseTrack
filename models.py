from views import mydb
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

CASE_CATEGORY = {
	1: 'Study visit',
	2: 'Dispensation',
	3: 'Internship',
	4: 'Course failure',
	5: 'Leave of absence'
}
CASE_STATUS = {
	1: 'Opened',
	2: 'Processing',
	3: 'Closed'
}

class User(mydb.Model):
	#__table__name = 'users'
	# risk overflow
	uid = mydb.Column(mydb.Integer, primary_key=True) 
	username = mydb.Column(mydb.String, unique=True, nullable = False)
	email = mydb.Column(mydb.String, unique=True, nullable = False)
	#pwdhash = db.Column(db.String, nullable = False)
	password = mydb.Column(mydb.String, nullable = False)
	cases = mydb.relationship('Case', backref='user')
	
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		#self.set_password(password)
		self.password = password

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	#def __repr__(self):
	#	return '<User %r>' % self.username

class Case(mydb.Model):
	#__table__name = 'cases'
	cid = mydb.Column(mydb.Integer, primary_key=True)
	category = mydb.Column(mydb.SmallInteger, nullable=False)
	resp_person = mydb.Column(mydb.String(40), nullable=False)
	status = mydb.Column(mydb.SmallInteger, nullable=False)
	opened = mydb.Column(mydb.Date, default = datetime.datetime.now())
	last_modified = mydb.Column(mydb.Date, nullable=False, default = datetime.datetime.now())
	user_id = mydb.Column(mydb.Integer, mydb.ForeignKey('user.uid'))

	def __init__(self, category, resp_person, status, user_id):
		self.category = category
		self.resp_person = resp_person
		self.status = status
		self.user_id = user_id

	def category_str(self):
		return CASE_CATEGORY[self.category]

	def status_str(self):
		return CASE_STATUS[self.status]

	#def __repr__(self):
	#	return '<Case %r>' % self.cid