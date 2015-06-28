# -*- coding: utf-8 -*-
import unittest
from flask.ext.testing import TestCase
from project import myapp, mydb
from project.models import Student, StudyProgram, Staff, StaffContact, StaffField, StaffTitle, Application, ProjectApp, Module, Company, CSupervisor, CSupervisorTitle, CSupervisorField, SupervisorApp, CASE_STATUS, CASE_PRIORITY, PROCESS_TIMEFRAME
import datetime

class ModelTestCase(TestCase):
	def create_app(self):
		myapp.config['TESTING'] = True
		myapp.config['DEBUG'] = True
		myapp.config['WTF_CSRF_ENABLED'] = False
		myapp.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:s122678@localhost:5433/scts_test"
		return myapp

	def setUp(self):
		mydb.create_all()

	def tearDown(self):
		mydb.session.remove()
		mydb.drop_all()

	def create_new_student(self):
		student = Student(
			study_no='s122678', 
			first_name='Chuan Xiang', 
			last_name='Gu', 
			birthdate=datetime.date(1900,1,1), 
			email='s122678@dtu.dk',
			password='1234567')
		mydb.session.add(student)
		mydb.session.commit()		
		return student

	def create_new_staff(self):
		staff = Staff(
			staff_id='bhch',
			first_name='Bo-Holst',
			last_name='Christensen',
			email='bhch@dtu.dk',
			password='1234567')
		mydb.session.add(staff)
		mydb.session.commit()
		return staff		
		
	def initialize_modules(self):
		module1 = Module(
					module_id=1,
					module_name='Final Thesis + Engineering Practice (15+15 ECTS)',
					module_ECTS='30')
		module2 = Module(
					module_id=2,
					module_name='Final Thesis (15 ects)',
					module_ECTS='15')		
		module3 = Module(
					module_id=3,
					module_name='Internship part 1 (15 ECTS)',
					module_ECTS='15')
		module4 = Module(
					module_id=4,
					module_name='Internship part 2 (15 ECTS)',
					module_ECTS='15')
		module5 = Module(
					module_id=5,
					module_name='Internship part 1+2 (30 ECTS)',
					module_ECTS='30')
		mydb.session.add(module1)
		mydb.session.add(module2)
		mydb.session.add(module3)
		mydb.session.add(module4)
		mydb.session.add(module5)
		mydb.session.commit()
		return 
	#Create new student and initialize_modules before calling this method
	def create_new_internship_app(self, student):	
		internship_app = ProjectApp(
			app_id=None,
			#created_datetime=datetime.datetime.now(),
			c_supervisor=None,
			u_supervisor=None,
			proj_module=2,
			proj_title='Social application intergration',
			proj_description='It\'s long story',
			proj_salary='No salary',
			proj_contract=None,
			proj_insurance=None,
			proj_s_date=datetime.date(2014,2,1), 
			proj_e_date=datetime.date(2014,5,30), 
			proj_h_date=datetime.date(2014,6,1),
			#deadline_datetime=datetime.datetime.today() + datetime.timedelta(days=PROCESS_TIMEFRAME[CASE_PRIORITY['Project app']]),			
			#std_comment=None,
			#std_document=None
			)
		internship_app.applicant_obj=student
		mydb.session.add(internship_app)
		mydb.session.commit()
		return internship_app

	def create_complete_internship_app(self):
		student = self.create_new_student()
		self.initialize_modules()
		internship_app = self.create_new_internship_app(student)
		company = Company(
			comp_name='Taxicaller',
			comp_address='Teknikringen 1A',
			comp_department='Development',
			comp_country='Sweden',
			comp_city='Linköping',
			comp_postcode='583 30',
			comp_web='http://www.taxicaller.com',
			comp_email='contact@taxicaller.com',
			comp_phone='+46 855921950'
			)
		c_supervisor = CSupervisor(
			c_sup_email='eero@taxicaller.com',
			c_sup_name='Eero',
			c_sup_phone='+46 855921950',
			comp_name='Taxicaller',
			comp_address='Teknikringen 1A',
			comp_department='Development',
			)
		#c_supervisor.company_obj = company
		c_supervisor_title1 = CSupervisorTitle(
			c_sup_email=c_supervisor.c_sup_email,
			c_sup_title='CEO'
			)
		c_supervisor_title2 = CSupervisorTitle(
			c_sup_email=c_supervisor.c_sup_email,
			c_sup_title='CFO'
			)		
		#c_supervisor_title.csupervisor_obj = c_supervisor

		c_supervisor_field = CSupervisorField(
			c_sup_email=c_supervisor.c_sup_email,
			c_sup_field='Web application'
			)
		#c_supervisor_field.csupervisor_obj = c_supervisor

		#internship_app.c_supervisor = c_supervisor.c_sup_email
		internship_app.csupervisor_obj = c_supervisor

		mydb.session.add(company)
		mydb.session.add(c_supervisor)
		mydb.session.add(c_supervisor_title1)
		mydb.session.add(c_supervisor_title2)
		mydb.session.add(c_supervisor_field)
		mydb.session.add(internship_app)
		mydb.session.commit()
		internship_app_rst = mydb.session.query(ProjectApp).filter_by(app_id=internship_app.app_id).first()
		self.assertIn(c_supervisor_title1, internship_app_rst.csupervisor_obj.csupervisortitle_list)
		return internship_app		

class MyModelTestCases(ModelTestCase):
	def test_new_student(self):
		student = self.create_new_student()
		student_rst = mydb.session.query(Student).first()
		self.assertEquals(student_rst, student)
		self.assertIs(student_rst, student)	

	def test_add_two_study_programs_to_student(self):
		student = self.create_new_student()
		student_rst_1 = mydb.session.query(Student).first()
		self.assertEquals(student_rst_1, student)
		self.assertIs(student_rst_1, student)
		study_program_1 = StudyProgram(
			study_no='s122678', 
			program='Foundation course',
			degree_type='Prepartory courses',
			reg_date=datetime.date(2011,9,1), 
			status='Graduated',
			earned_ECTs='60',
			reg_ECTs='0',
			tot_ECTs='60',
			graduation_date=datetime.date(2012,7,1)			
			)
		study_program_2 = StudyProgram(
			study_no='s122678', 
			program='IT',
			degree_type='DTU Diploma',
			reg_date=datetime.date(2012,9,1), 
			status='On campus',
			earned_ECTs='295',
			reg_ECTs='20',
			tot_ECTs='310',
			graduation_date=datetime.date(2015,7,1)			
			)
		student_rst_1.studyprogram_list=[study_program_1, study_program_2]
		mydb.session.add(student_rst_1)
		mydb.session.commit()
		student_rst_2 = mydb.session.query(Student).filter_by(study_no='s122678').one()
		self.assertIs(student_rst_2, student_rst_1)
		self.assertIn(study_program_1, student_rst_2.studyprogram_list)
		self.assertIn(study_program_2, student_rst_2.studyprogram_list)		

	def test_new_staff(self):
		staff = self.create_new_staff()
		staff_rst = mydb.session.query(Staff).first()
		self.assertEquals(staff_rst, staff)
		self.assertIs(staff_rst, staff)	

	def test_add_two_contacts_to_new_staff(self):
		staff = self.create_new_staff()
		staff_rst1 = mydb.session.query(Staff).first()
		self.assertEquals(staff_rst1, staff)
		self.assertIs(staff_rst1, staff)	
		contact_1 = StaffContact(
			staff_id='bhch',
			department='DTU DIPLOM',
			office='X1.54',
			phone='35885113'
			)
		contact_2 = StaffContact(
			staff_id='bhch',
			department='DTU COMPUTE',
			office='C1.23',
			phone='44805113'
			)					
		staff_rst1.contact_list=[contact_1, contact_2]
		mydb.session.add(staff_rst1)
		mydb.session.commit()
		staff_rst2 = mydb.session.query(Staff).filter_by(staff_id='bhch').first()
		self.assertIn(contact_1, staff_rst2.contact_list)
		self.assertIn(contact_2, staff_rst2.contact_list)

	def test_add_projectapp_to_student(self):
		student = self.create_new_student()
		self.initialize_modules()
		internship_app = self.create_new_internship_app(student)
		internship_app_rst = mydb.session.query(ProjectApp).one()
		self.assertIs(internship_app_rst, internship_app)
		self.assertEquals(internship_app_rst.module_obj.module_ECTS, '15')

	def test_add_company_supervisor_to_projectapp(self):
		student = self.create_new_student()
		self.initialize_modules()
		internship_app = self.create_new_internship_app(student)
		company = Company(
			comp_name='Taxicaller',
			comp_address='Teknikringen 1A',
			comp_department='Development',
			comp_country='Sweden',
			comp_city='Linköping',
			comp_postcode='583 30',
			comp_web='http://www.taxicaller.com',
			comp_email='contact@taxicaller.com',
			comp_phone='+46 855921950'
			)
		c_supervisor = CSupervisor(
			c_sup_email='eero@taxicaller.com',
			c_sup_name='Eero',
			c_sup_phone='+46 855921950',
			comp_name='Taxicaller',
			comp_address='Teknikringen 1A',
			comp_department='Development',
			)
		c_supervisor.company_obj = company
		c_supervisor_title = CSupervisorTitle(
			c_sup_email=c_supervisor.c_sup_email,
			c_sup_title='CEO'
			)
		c_supervisor_title.csupervisor_obj = c_supervisor

		c_supervisor_field = CSupervisorField(
			c_sup_email=c_supervisor.c_sup_email,
			c_sup_field='Web application'
			)
		c_supervisor_field.csupervisor_obj = c_supervisor

		#internship_app.c_supervisor = c_supervisor.c_sup_email
		internship_app.csupervisor_obj = c_supervisor

		mydb.session.add(company)
		mydb.session.add(c_supervisor)
		mydb.session.add(c_supervisor_title)
		mydb.session.add(c_supervisor_field)
		mydb.session.add(internship_app)
		mydb.session.commit()

		internship_app_rst = mydb.session.query(ProjectApp).one()
		self.assertIs(internship_app_rst, internship_app)
		self.assertEquals(internship_app_rst.module_obj.module_ECTS, '15')
		self.assertIs(internship_app_rst.csupervisor_obj, c_supervisor)	
		self.assertIs(internship_app_rst.csupervisor_obj.csupervisortitle_list[0], c_supervisor_title)	
		self.assertEquals(internship_app_rst.c_supervisor, c_supervisor.c_sup_email)	

	#incomplete	
	def test_delete_projectapp_from_student(self):
		student = self.create_new_student()
		self.initialize_modules()
		internship_app = self.create_new_internship_app(student)
		internship_app_rst = mydb.session.query(ProjectApp).one()
		#self.assertIs(internship_app_rst, internship_app)
		mydb.session.delete(internship_app_rst)
		mydb.session.commit()
		self.assertIsNone(mydb.session.query(ProjectApp).first())

	def test_save_projectapp_to_student(self):
		student = self.create_new_student()
		self.initialize_modules()
		internship_app = ProjectApp(
			app_id=None,
			#created_datetime=datetime.datetime.now(),
			c_supervisor=None,
			u_supervisor=None,
			proj_module=2,
			proj_title='Social application intergration',
			proj_description='It\'s long story',
			proj_salary='No salary',
			proj_contract=None,
			proj_insurance=None,
			proj_s_date=None, 
			proj_e_date=None, 
			proj_h_date=None,
			#deadline_datetime=datetime.datetime.today() + datetime.timedelta(days=PROCESS_TIMEFRAME[CASE_PRIORITY['Project app']]),
			#std_comment=None,
			#std_document=None
			)
		internship_app.applicant_obj=student
		app_id_rst = internship_app.std_save()
		#print 'app_id: %d' % app_id_rst
		internship_app_rst = mydb.session.query(ProjectApp).filter_by(app_id=app_id_rst).one()
		self.assertIs(internship_app_rst, internship_app)
		self.assertEquals(internship_app_rst.module_obj.module_ECTS, '15')

	def test_apply_projectapp(self):		
		internship_app = self.create_complete_internship_app()
		internship_app.apply()
		internship_app_rst = mydb.session.query(ProjectApp).filter_by(applicant=internship_app.applicant, created_datetime=internship_app.created_datetime).one()
		self.assertIs(internship_app_rst, internship_app)
		self.assertEquals(internship_app_rst.case_status, 'Applied')	

	def test_add_projectapp_to_staff(self):
		internship_app = self.create_complete_internship_app()
		internship_app_rst1 = mydb.session.query(ProjectApp).filter_by(app_id=internship_app.app_id).one()
		staff = self.create_new_staff()
		internship_app_rst1.case_owner_obj = staff
		internship_app_rst1.app_description = 'Oversea internshp, Sweden'
		case_priority = CASE_PRIORITY['PROJECT_APP']
		case_status = 'Accepted'
		mydb.session.add(internship_app_rst1)
		mydb.session.commit()
		internship_app_rst2 = mydb.session.query(ProjectApp).filter_by(app_id=internship_app.app_id).one()
		self.assertIs(internship_app_rst2, internship_app_rst1)
		self.assertEquals(internship_app_rst2, internship_app_rst1)

	def test_accept_projectapp(self):
		internship_app = self.create_complete_internship_app()
		#print 'app_id: %d' % internship_app.app_id
		staff = self.create_new_staff()
		internship_app.accept(staff.staff_id)
		internship_app_rst = mydb.session.query(ProjectApp).filter_by(app_id=internship_app.app_id).one()
		self.assertEquals(internship_app_rst.case_status, 'Accepted')


if __name__ == "__main__":
		unittest.main()
