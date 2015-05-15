from project import mydb
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

CASE_CATEGORY = {
	1: 'Study visit',
	2: 'Dispensation',
	3: 'Project',
	4: 'Course failure',
	5: 'Leave of absence'
}
CASE_STATUS = {
	1: 'Opened',
	2: 'Processing',
	3: 'Closed'
}
CASE_PRIORITY = {
	1: 'lOW',
	2: 'INTERMEDIATE',
	3: 'HIGH'
}

STUDY_STATUS = {
	1: 'On campus course',
	2: 'On internship',
	3: 'Study abroad',
	4: 'Guest student',
	5: 'On thesis',
	6: 'On leave',
	7: 'Inactive',
	8: 'Terminated'
}

DEGREE_TYPE = {
	1: 'Bachelor',
	2: 'Master',
	3: 'Diploma',
	4: 'Admission course',
	5: 'Guest student',
	6: 'Exchange student',
	7: 'Continuning education'
}

PROGRAM = {
	1: 'Architectural Engineering',
	2: 'Arctic Technology',
	3: 'Building and Civil Engineering',
	4: 'Chemical and biochemical Engineering',
	5: 'Chemistry and Business Economy',
	6: 'Electrical Engineering',
	7: 'Electrical Energy Technology',
	8: 'Food Analysis',
	9: 'Global Business Engineering',
	10: 'Healthcare Technology',
	11: 'IT and Economics',
	12: 'IT Electronics',
	13: 'Manufacturing and Management',
	14: 'Mechanical Engineering',
	15: 'Process and Innovation',
	16: 'Software Technology',
	17: 'Traffic and Transportation'
}

DEPARTMENT = {
	1: 'Administrative Department',
	2: 'Advisory Board',
	3: 'Board os Studies',
	4: 'Center for Continuing Educaiton',
	5: 'Center for Innovation',
	6: 'DTU Admission Course',
	7: 'Educational Committee',
	8: 'Section of Buidling and infrastructure',
	9: 'Section of  Eletric Technology',
  10: 'Section of Informatics',
  11: 'Section of Mechnical Engineering and Design',
  12: 'Section of Business Development',
  13: 'Section of Production Development',
  14: 'Workshop and Labortaries'
}

PROJ_MODULE = {
	1: 'Final Thesis + Engineering Practice (15+15 ects)',
	2: 'Final Thesis (15 ects)',
	3: 'Internship part 1 (15 credits)',
	4: 'Internship part 2 (15 credits)',
	5: 'Internship part 1+2 (30 credits)'
}


class User(mydb.Model):
	__tablename__ = 'users'
	# risk overflow
	uid = mydb.Column(mydb.Integer, primary_key=True) 
	username = mydb.Column(mydb.String, unique=True, nullable = False)
	email = mydb.Column(mydb.String, unique=True, nullable = False)
	#pwdhash = db.Column(db.String, nullable = False)
	password = mydb.Column(mydb.String, nullable = False)
	cases = mydb.relationship('Case', backref='users')
	
	def __init__(self, 
		username, 
		email, 
		password):
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
	__tablename__ = 'cases'
	cid = mydb.Column(mydb.Integer, primary_key=True)
	category = mydb.Column(mydb.SmallInteger, nullable=False)
	resp_person = mydb.Column(mydb.String, nullable=False)
	status = mydb.Column(mydb.SmallInteger, nullable=False)
	opened = mydb.Column(mydb.Date, default = datetime.datetime.now())
	last_modified = mydb.Column(mydb.Date, nullable=False, default = datetime.datetime.now())
	user_id = mydb.Column(mydb.Integer, mydb.ForeignKey('users.uid'))

	def __init__(self, 
		category, 
		resp_person, 
		status, 
		user_id):
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

class Student(mydb.Model):
	__tablename__ = 'STUDENT'
	study_no = mydb.Column(mydb.String(20), primary_key = True) #study_no = mydb.Column(mydb.String(20), primary_key = True)
	std_first_name = mydb.Column(mydb.String(64))
	std_last_name = mydb.Column(mydb.String(64))
	std_birthdate = mydb.Column(mydb.Date())
	std_email = mydb.Column(mydb.String(62))
	std_password = mydb.Column(mydb.String())
	study_programs = mydb.relationship('StudyProgram', backref='student')
	project_apps = mydb.relationship('ProjectApp', backref='student')

	def __init__(
		self, 
		study_no, 
		std_first_name, 
		std_last_name, 
		std_birthdate, 
		std_email, 
		std_password
		):
		self.study_no = study_no
		self.std_first_name = std_first_name
		self.std_last_name = std_last_name
		self.std_birthdate = std_birthdate
		self.std_email = std_email
		self.std_password = std_password

	def __repr__(self):
		return '<Student (%s %s %s)>' % (self.study_no, self.study_programs, self.project_apps)

class StudyProgram(mydb.Model):
	__tablename__ = 'STUDY_PROGRAM'
	study_no = mydb.Column(mydb.String(20), mydb.ForeignKey('STUDENT.study_no'), primary_key = True)
	program = mydb.Column(mydb.String(100), primary_key = True)
	degree_type = mydb.Column(mydb.String(8), primary_key = True)
	reg_date = mydb.Column(mydb.Date())
	status = mydb.Column(mydb.String(20))
	earned_ECTs = mydb.Column(mydb.String(5))
	reg_ECTs = mydb.Column(mydb.String(4))
	tot_ECTs = mydb.Column(mydb.String(5))
	graduation_date = mydb.Column(mydb.Date())

	def __init__(
		self,
		study_no,
		program,
		degree_type,
		reg_date,
		status,
		earned_ECTs,
		reg_ECTs,
		tot_ECTs,
		graduation_date
		):
		self.study_no = study_no
		self.program = program
		self.degree_type = degree_type
		self.reg_date = reg_date
		self.status = status
		self.earned_ECTs = earned_ECTs
		self.reg_ECTs = reg_ECTs
		self.tot_ECTs = tot_ECTs
		self.graduation_date = graduation_date

	def program_str(self):
		return PROGRAM[self.program]

	def degree_type_str(self):
		return DEGREE_TYPE[self.degree_type]


class Staff(mydb.Model):
	__tablename__ = 'STAFF'
	staff_id = mydb.Column(mydb.String(20), primary_key = True)
	staff_first_name = mydb.Column(mydb.String(64))
	staff_last_name = mydb.Column(mydb.String(64))
	staff_email = mydb.Column(mydb.String(62))
	staff_password = mydb.Column(mydb.String())
	staff_contacts = mydb.relationship('StaffContact', backref='staff')
	staff_fields = mydb.relationship('StaffField', backref='staff')
	staff_titles = mydb.relationship('StaffTitle', backref='staff')
	project_apps = mydb.relationship('ProjectApp', backref='staff')
	app_u_supervisors = mydb.relationship('AppUSupervisor', backref='staff')

	def __init__(
		self,
		staff_id,
		staff_first_name,
		staff_last_name,
		staff_email,
		staff_password
		):
		self.staff_id = staff_id
		self.staff_first_name = staff_first_name
		self.staff_last_name = staff_last_name
		self.staff_email = staff_email
		self.staff_password = staff_password

class StaffContact(mydb.Model):
	__tablename__ = 'STAFF_CONTACT'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	staff_department = mydb.Column(mydb.String(50), primary_key = True)
	staff_office = mydb.Column(mydb.String(50))
	staff_phone = mydb.Column(mydb.String(15))

	def __init__(
		self,
		staff_id,
		staff_department,
		staff_office,
		staff_phone
		):
		self.staff_id = staff_id
		self.staff_department = staff_department
		self.staff_office = staff_office
		self.staff_phone = staff_phone

class StaffField(mydb.Model):
	__tablename__ = 'STAFF_FIELD'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	staff_field  = mydb.Column(mydb.String(100), primary_key = True)

	def __init__(
		self,
		staff_id,
		staff_field):
		self.staff_id = staff_id
		self.staff_field = staff_field

class StaffTitle(mydb.Model):
	__tablename__ = 'STAFF_TITLE'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	staff_title  = mydb.Column(mydb.String(50), primary_key = True)

	def __init__(
		self,
		staff_id,
		staff_title):
		self.staff_id = staff_id
		self.staff_title = staff_title

class ProjectApp(mydb.Model):
	__tablename__ = 'PROJECT_APP'
	app_id = mydb.Column(mydb.Integer, primary_key = True)#app_id = mydb.Column(mydb.String(30), primary_key = True)
	study_no = mydb.Column(mydb.String(20), mydb.ForeignKey('STUDENT.study_no'))
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id')) 
	app_description = mydb.Column(mydb.Text())
	app_category = mydb.Column(mydb.String(30))
	case_priority  = mydb.Column(mydb.String(20))
	case_status  = mydb.Column(mydb.String(10))
	case_owner  = mydb.Column(mydb.String(70))
	std_comment = mydb.Column(mydb.Text())
	std_document = mydb.Column(mydb.LargeBinary())
	app_decision = mydb.Column(mydb.String(10))
	staff_comment = mydb.Column(mydb.Text())
	staff_document = mydb.Column(mydb.LargeBinary())
	created_datetime = mydb.Column(mydb.Date())
	deadline_datetime = mydb.Column(mydb.Date())
	close_datetime = mydb.Column(mydb.Date())
	comp_name = mydb.Column(mydb.String(50))
	comp_address = mydb.Column(mydb.String(95))
	comp_department = mydb.Column(mydb.String(50))
	c_sup_email = mydb.Column(mydb.String(62))
	proj_module = mydb.Column(mydb.String(20))
	proj_ECTs = mydb.Column(mydb.String(4))
	proj_title = mydb.Column(mydb.Text())
	proj_description = mydb.Column(mydb.Text())
	proj_salary = mydb.Column(mydb.Text())
	proj_contract = mydb.Column(mydb.LargeBinary())
	proj_insurance = mydb.Column(mydb.LargeBinary())
	proj_s_date = mydb.Column(mydb.Date())
	proj_e_date = mydb.Column(mydb.Date())
	proj_h_date = mydb.Column(mydb.Date())
	u_sup_name = mydb.Column(mydb.String(70))
	app_u_supervisors = mydb.relationship('AppUSupervisor', backref='projectApp')
	
	def __init__(
		self,
		app_description,
		proj_module,
		proj_ECTs,
		proj_title,
		proj_description,
		proj_salary,
		proj_contract,
		proj_insurance,
		proj_s_date,
		proj_e_date
		):
		#call a function to generate app_id
		self.app_id = None
		self.study_no = None
		self.staff_id = None
		self.app_description = app_description
		self.app_category = CASE_CATEGORY[3]
		self.case_priority = CASE_PRIORITY[1]
		self.case_status = CASE_STATUS[1]
		self.case_owner = None
		self.std_comment = None
		self.std_document = None
		self.app_decision = None
		self.created_datetime = datetime.datetime.now() #created_datetime
		self.deadline_datetime = None
		self.close_datetime = None
		self.comp_name = None
		self.comp_address = None
		self.comp_department = None
		self.c_sup_email = None
		self.proj_module = proj_module
		self.proj_ECTs = proj_ECTs
		self.proj_title = proj_title
		self.proj_description = proj_description
		self.proj_salary = proj_salary
		self.proj_contract = proj_contract
		self.proj_insurance = proj_insurance
		self.proj_s_date = proj_s_date
		self.proj_e_date = proj_e_date
		self.proj_h_date = None
		self.u_sup_name = None



class Company(mydb.Model):
	__tablename__ = 'COMPANY'
	comp_name = mydb.Column(mydb.String(50), primary_key = True)
	comp_address = mydb.Column(mydb.String(95), primary_key = True)
	comp_department = mydb.Column(mydb.String(50), primary_key = True)
	comp_country = mydb.Column(mydb.String(90))
	comp_city = mydb.Column(mydb.String(60))
	comp_postcode = mydb.Column(mydb.String(10))
	comp_web = mydb.Column(mydb.Text())
	comp_email = mydb.Column(mydb.String(62))
	comp_phone = mydb.Column(mydb.String(15))
	csupervisors = mydb.relationship('CSupervisor', backref='company')

	def __init__(
		self,
		comp_name,
		comp_address,
		comp_department,
		comp_country,
		comp_city,
		comp_postcode,
		comp_web,
		comp_email,
		comp_phone
		):
		self.comp_name = comp_name
		self.comp_address = comp_address
		self.comp_department = comp_department
		self.comp_country = comp_country
		self.comp_city = comp_city
		self.comp_postcode = comp_postcode
		self.comp_web = comp_web
		self.comp_email = comp_email
		self.comp_phone = comp_phone

class CSupervisor(mydb.Model):
	__tablename__ = 'C_SUPERVISOR'
	c_sup_email = mydb.Column(mydb.String(62), primary_key = True)
	c_sup_name = mydb.Column(mydb.String(70))
	c_sup_phone = mydb.Column(mydb.String(15))
	comp_name = mydb.Column(mydb.String(50))
	comp_address = mydb.Column(mydb.String(95))
	comp_department = mydb.Column(mydb.String(50))	
	c_supervisors_titles = mydb.relationship('CSupervisorTitle', backref='cSupervisor')
	c_supervisors_fields = mydb.relationship('CSupervisorField', backref='cSupervisor')
	__table_args__ = (
		mydb.ForeignKeyConstraint(
			['comp_name','comp_address', 'comp_department'],
			['COMPANY.comp_name', 'COMPANY.comp_department', 'COMPANY.comp_address']
			),
		)

	def __init__(
		self,
		c_sup_email,
		c_sup_name,
		c_sup_phone,
		comp_name,
		comp_address,
		comp_department,
		):
		self.c_sup_email = c_sup_email
		self.c_sup_name = c_sup_name
		self.c_sup_phone = c_sup_phone
		self.comp_name = comp_name
		self.comp_address = comp_address
		self.comp_department = comp_department

class CSupervisorTitle(mydb.Model):
	__tablename__ = 'C_SUPERVISOR_TITLE'
	c_sup_email = mydb.Column(mydb.String(62), mydb.ForeignKey('C_SUPERVISOR.c_sup_email'), primary_key = True)
	c_sup_title = mydb.Column(mydb.String(50), primary_key = True)

	def __init__(
		self,
		c_sup_email,
		c_sup_title
		):
		self.c_sup_email = c_sup_email
		self.c_sup_title = c_sup_title

class CSupervisorField(mydb.Model):
	__tablename__ = 'C_SUPERVISOR_FIELD'
	c_sup_email = mydb.Column(mydb.String(62), mydb.ForeignKey('C_SUPERVISOR.c_sup_email'), primary_key = True)
	c_sup_field = mydb.Column(mydb.String(100), primary_key = True)

	def __init__(
		self,
		c_sup_email,
		c_sup_field
		):
		self.c_sup_email = c_sup_email
		self.c_sup_field = c_sup_field

class AppUSupervisor(mydb.Model):
	__tablename__ = 'APP_U_SUPERVISOR'
	app_id = mydb.Column(mydb.Integer, mydb.ForeignKey('PROJECT_APP.app_id'), primary_key = True)
	app_u_sup_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	app_priority = mydb.Column(mydb.String(20))

	def __init__(
		self,
		app_id,
		app_u_sup_id,
		app_priority
		):
		self.app_id = app_id
		self.app_u_sup_id = app_u_sup_id
		self.app_priority = app_priority

class File(mydb.Model):
	__tablename__ = 'FILE'
	id = mydb.Column(mydb.Integer, primary_key = True)
	filename = mydb.Column(mydb.String(64), nullable = False)
	filesize = mydb.Column(mydb.Integer, nullable = False)
	created = mydb.Column(mydb.TIMESTAMP(True), nullable = False)
	filedata = mydb.relationship('FileData', backref='file')

class FileData(mydb.Model):
	__tablename__ = 'FILE_DATA'
	file_id = mydb.Column(mydb.Integer, mydb.ForeignKey('FILE.id'), primary_key = True)
	segment = mydb.Column(mydb.String, primary_key = True)
	data = 	mydb.Column(mydb.LargeBinary)
