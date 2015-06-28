from project import mydb, bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from sqlalchemy.schema import Index 
from sqlalchemy.orm import backref
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

CASE_CATEGORY = {
	1: 'Study visit',
	2: 'Dispensation',
	3: 'Project',
	4: 'Course failure',
	5: 'Leave of absence'
}
CASE_STATUS = {
	1: 'Rejected',
	2: 'Accepted', 
	3: 'Processing',
	4: 'Closed',
	5: 'Reopened',
	6: 'Applied'
}

DECISION = {
	1: 'Preapprove',
	2: 'Approve',
	3: 'Reject'
}

CASE_PRIORITY = {
	'LEAVE_ABSENCE_APP': 'Low',
	'STUDY_VISIT_APP': 'Low',
	'PROJECT_APP': 'High',
	'SUPERVISOR_APP': 'High',
	'DIPENSATION_APP': 'Medium',
}

PROCESS_TIMEFRAME = {
	'Low': 21,
	'Medium':14,
	'High':7 
}

STUDY_STATUS = {
	1: 'Full-time in house',
	2: 'Full-time project',
	3: 'Part-time project, part-time in house',
	4: 'Study abroad',
	5: 'Guest student',
	6: 'On thesis',
	7: 'On leave',
	8: 'Inactive',
	9: 'Terminated',
	10: 'Graduated'
}

DEGREE_TYPE = {
	1: 'Bachelor of Science',
	2: 'Master of Engineering',
	3: 'Bachelor of Engineering',
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
	17: 'Traffic and Transportation',
	18: 'Admission course'
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
'''
PROJ_MODULE = {
	1: 'Final Thesis + Engineering Practice (15+15 ECTS)',
	2: 'Final Thesis (15 ects)',
	3: 'Internship part 1 (15 ECTS)',
	4: 'Internship part 2 (15 ECTS)',
	5: 'Internship part 1+2 (30 ECTS)'
}
'''

class Student(mydb.Model):
	__tablename__ = 'STUDENT'
	__table_args__ = (Index('SearchNameIndices', "last_name", "first_name"), )
	study_no = mydb.Column(mydb.String(20), primary_key = True) 
	first_name = mydb.Column(mydb.String(64))
	last_name = mydb.Column(mydb.String(64)) 
	birthdate = mydb.Column(mydb.Date(), index=True)
	email = mydb.Column(mydb.String(62), unique=True, nullable = False)
	password = mydb.Column(mydb.String(), nullable = False)
	
	def __init__(
		self, 
		study_no, 
		first_name, 
		last_name, 
		birthdate, 
		email, 
		password
		):
		self.study_no = study_no
		self.first_name = first_name
		self.last_name = last_name
		self.birthdate = birthdate
		self.email = email
		self.password = bcrypt.generate_password_hash(password)

	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.study_no)		

#Index('SearchNameIndices',Student.last_name, Student.first_name)

class StudyProgram(mydb.Model):
	__tablename__ = 'STUDY_PROGRAM'
	study_no = mydb.Column(mydb.String(20), mydb.ForeignKey('STUDENT.study_no'), primary_key = True)
	program = mydb.Column(mydb.String(100), primary_key = True)
	degree_type = mydb.Column(mydb.String(30), primary_key = True)
	reg_date = mydb.Column(mydb.Date())
	status = mydb.Column(mydb.String(40))
	earned_ECTs = mydb.Column(mydb.String(5))
	reg_ECTs = mydb.Column(mydb.String(4))
	tot_ECTs = mydb.Column(mydb.String(5))
	graduation_date = mydb.Column(mydb.Date())
	student_obj = mydb.relationship('Student', 
		backref=backref('studyprogram_list', cascade='all, delete-orphan'))

	def program_str(self):
		return PROGRAM[self.program]

	def degree_type_str(self):
		return DEGREE_TYPE[self.degree_type]

class Staff(mydb.Model):
	__tablename__ = 'STAFF'
	staff_id = mydb.Column(mydb.String(20), primary_key = True)
	first_name = mydb.Column(mydb.String(64))
	last_name = mydb.Column(mydb.String(64))
	email = mydb.Column(mydb.String(62), unique=True, nullable = False)
	password = mydb.Column(mydb.String(), nullable = False)

	role = mydb.Column(mydb.String(30))
	__mapper_args__ = {
			'polymorphic_identity':'APPLICATION',
			'polymorphic_on':role
	}

	def __init__(
		self,
		staff_id,
		first_name,
		last_name,
		email,
		password
		):
		self.staff_id = staff_id
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = bcrypt.generate_password_hash(password)

	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.staff_id)				

class ProjectUSupervisor(Staff):
	__tablename__ = 'PROJECT_U_SUPERVISOR'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	name = mydb.Column(mydb.String(128)) 
	__mapper_args__ = {
			'polymorphic_identity':'PROJECT_U_SUPERVISOR',
	}

class StaffContact(mydb.Model):
	__tablename__ = 'STAFF_CONTACT'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	department = mydb.Column(mydb.String(50), primary_key = True)
	office = mydb.Column(mydb.String(50))
	phone = mydb.Column(mydb.String(15))
	staff_obj = mydb.relationship('Staff', backref='contact_list')

class StaffField(mydb.Model):
	__tablename__ = 'STAFF_FIELD'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	field  = mydb.Column(mydb.String(100), primary_key = True)
	staff_obj = mydb.relationship('Staff', 
		backref=backref('field_list', cascade='all, delete-orphan'))

class StaffTitle(mydb.Model):
	__tablename__ = 'STAFF_TITLE'
	staff_id = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'), primary_key = True)
	title  = mydb.Column(mydb.String(50), primary_key = True)
	staff_obj = mydb.relationship('Staff',
		backref=backref('title_list', cascade='all, delete-orphan'))

class Application(mydb.Model):
	__tablename__ = 'APPLICATION'		
	app_id = mydb.Column(mydb.Integer, primary_key = True)#app_id = mydb.Column(mydb.String(30), primary_key = True)
	created_datetime = mydb.Column(mydb.DateTime(), primary_key = True, default=datetime.datetime.now)
	case_owner = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id')) 
	applicant = mydb.Column(mydb.String(20), mydb.ForeignKey('STUDENT.study_no'))
	app_description = mydb.Column(mydb.Text())
	case_priority  = mydb.Column(mydb.String(20))
	case_status  = mydb.Column(mydb.String(10))
	app_decision = mydb.Column(mydb.String(15))
	submitted_datetime = mydb.Column(mydb.DateTime())
	deadline_datetime = mydb.Column(mydb.DateTime())
	close_datetime = mydb.Column(mydb.DateTime())	
	std_comment = mydb.Column(mydb.Text())
	std_document = mydb.Column(mydb.LargeBinary())
	staff_comment = mydb.Column(mydb.Text())
	staff_document = mydb.Column(mydb.LargeBinary())

	app_category = mydb.Column(mydb.String(30))
	applicant_obj = mydb.relationship('Student', backref='application_list')
	case_owner_obj = mydb.relationship('Staff', backref='application_list')
	__mapper_args__ = {
			'polymorphic_identity':'APPLICATION',
			'polymorphic_on':app_category
	}

proj_ass_u_sup_table = mydb.Table('PROJECT_ASSOCIATE_U_SUPERVISOR', 
	mydb.Column('staff_id', mydb.String(20), mydb.ForeignKey('STAFF.staff_id')),
	mydb.Column('app_id', mydb.Integer),
	mydb.Column('created_datetime', mydb.DateTime()),
	mydb.ForeignKeyConstraint(
		['app_id','created_datetime'],
		['PROJECT_APP.app_id', 'PROJECT_APP.created_datetime'])
	)

class ProjectApp(Application):
	__tablename__ = 'PROJECT_APP'	
	__table_args__ = (
		mydb.ForeignKeyConstraint(
			['app_id','created_datetime'],
			['APPLICATION.app_id', 'APPLICATION.created_datetime']
			),				
		)	
	app_id = mydb.Column(mydb.Integer, primary_key = True)
	created_datetime = mydb.Column(mydb.DateTime(), primary_key = True)
	c_supervisor = mydb.Column(mydb.String(62), mydb.ForeignKey('C_SUPERVISOR.c_sup_email'))
	u_supervisor = mydb.Column(mydb.String(20), mydb.ForeignKey('STAFF.staff_id'))
	proj_module = mydb.Column(mydb.Integer, mydb.ForeignKey('MODULE.module_id'))	
	proj_title = mydb.Column(mydb.Text())
	proj_description = mydb.Column(mydb.Text())
	proj_salary = mydb.Column(mydb.Text())
	proj_contract = mydb.Column(mydb.LargeBinary())
	proj_insurance = mydb.Column(mydb.LargeBinary())
	proj_s_date = mydb.Column(mydb.Date())
	proj_e_date = mydb.Column(mydb.Date())
	proj_h_date = mydb.Column(mydb.Date())
	csupervisor_obj = mydb.relationship('CSupervisor', backref='projectapp_list')
	usupervisor_obj = mydb.relationship('Staff', backref='projectapp_list')
	module_obj = mydb.relationship('Module', backref='projectapp_list')
	project_usupervisor_list = mydb.relationship('ProjectUSupervisor', secondary=proj_ass_u_sup_table,
        backref=mydb.backref('projectapp_offer_list', lazy='dynamic'))
	__mapper_args__ = {
			'polymorphic_identity':'PROJECT_APP',
	}
	#use app_id for query in the future
	def std_save(self):
		mydb.session.add(self)
		mydb.session.commit()
		try:
			projectApp = mydb.session.query(ProjectApp).filter_by(
				applicant=self.applicant, created_datetime=self.created_datetime).one()	
		except NoResultFound, e:
			print e
		except MultipleResultsFound, e:
			print e #or direct to error page
		return projectApp.app_id

	def apply(self):
		self.case_status = 'Applied'
		self.submitted_datetime = datetime.datetime.today()
		self.deadline_datetime= datetime.datetime.today()
		+ datetime.timedelta(days=PROCESS_TIMEFRAME[CASE_PRIORITY[self.app_category]])
		self.case_priority = CASE_PRIORITY[self.app_category]
		mydb.session.add(self)
		mydb.session.commit()

	def get_decision(self):
		try:
			projectApp = mydb.session.query(ProjectApp).filter_by(
				app_id=self.app_id).one()
		except NoResultFound, e:
			print e
		except MultipleResultsFound, e:
			print e #or direct to error page			
		return projectApp.app_decision

	def stf_save(self):
		mydb.session.add(self)
		mydb.session.commit()

	def accept(self, staff_id):
		self.case_status = 'Accepted'
		self.case_owner = staff_id
		self.stf_save()

	def reject(self, staff, staff_comment_txt):
		self.case_status = 'Rejected'
		self.case_owner = staff.staff_id
		self.staff_comment = staff_comment_txt
		self.stf_save()		

	#def transfer_to(self, staff, staff_comment_txt):

	def close(self):
		self.close_datetime = datetime.datetime.now()
		self.set_case_status('Closed')

	def reopen(self):
		self.submitted_datetime = datetime.datetime.now() 
		self.set_case_status('Reopened')

	def set_case_status(self, status):
		self.case_status = status
		self.stf_save()	


class Module(mydb.Model):
	__tablename__= 'MODULE'
	module_id = mydb.Column(mydb.Integer, primary_key = True)
	module_name = mydb.Column(mydb.String(60))
	module_ECTS = mydb.Column(mydb.String(4))	

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

	def stf_save(self):
		mydb.session.add(self)
		mydb.session.commit()	

class CSupervisor(mydb.Model):
	__tablename__ = 'C_SUPERVISOR'
	c_sup_email = mydb.Column(mydb.String(62), primary_key = True)
	c_sup_name = mydb.Column(mydb.String(70))
	c_sup_phone = mydb.Column(mydb.String(15))
	comp_name = mydb.Column(mydb.String(50))
	comp_address = mydb.Column(mydb.String(95))
	comp_department = mydb.Column(mydb.String(50))	
	company_obj = mydb.relationship('Company',
		backref=backref('csupervisor_list', cascade='all, delete-orphan'))
	__table_args__ = (
		mydb.ForeignKeyConstraint(
			['comp_name','comp_address', 'comp_department'],
			['COMPANY.comp_name', 'COMPANY.comp_address', 'COMPANY.comp_department']
			),
		)

	def stf_save(self):
		mydb.session.add(self)
		mydb.session.commit()

class CSupervisorTitle(mydb.Model):
	__tablename__ = 'C_SUPERVISOR_TITLE'
	c_sup_email = mydb.Column(mydb.String(62), mydb.ForeignKey('C_SUPERVISOR.c_sup_email'), primary_key = True)
	c_sup_title = mydb.Column(mydb.String(50), primary_key = True)
	csupervisor_obj = mydb.relationship('CSupervisor', 
		backref=backref('csupervisortitle_list', cascade='all, delete-orphan'))

	def stf_save(self):
		mydb.session.add(self)
		mydb.session.commit()	

class CSupervisorField(mydb.Model):
	__tablename__ = 'C_SUPERVISOR_FIELD'
	c_sup_email = mydb.Column(mydb.String(62), mydb.ForeignKey('C_SUPERVISOR.c_sup_email'), primary_key = True)
	c_sup_field = mydb.Column(mydb.String(100), primary_key = True)
	csupervisor_obj = mydb.relationship('CSupervisor',
		backref=backref('csupervisorfield_list', cascade='all, delete-orphan'))

	def stf_save(self):
		mydb.session.add(self)
		mydb.session.commit()	

class SupervisorApp(Application):
	__tablename__ = 'SUPERVISOR_APP'
	__table_args__ = (
		mydb.ForeignKeyConstraint(
			['app_id','created_datetime'],
			['APPLICATION.app_id', 'APPLICATION.created_datetime']
			),				
		)	
	app_id = mydb.Column(mydb.Integer, primary_key = True)
	created_datetime = mydb.Column(mydb.DateTime(), primary_key = True)
	app_priority = mydb.Column(mydb.String(20))
	__mapper_args__ = {
			'polymorphic_identity':'SUPERVISOR_APP',
	}



