# -*- coding: utf-8 -*-
from project import mydb
from project.models import Staff, Module, Student, StudyProgram, Staff, StaffContact, StaffField, StaffTitle
import datetime

# create the database and the table
mydb.drop_all()
mydb.create_all()
admin = Staff(
			staff_id = 'admin', 
			first_name="Xiang", 
			last_name="Gu", 
			email="admin@dtu.dk", 
			password="123456")

hebec = Staff(
			staff_id='hebec',
			first_name='Henrik',
			last_name='Bechmann',
			email='hebec@dtu.dk',
			password='1234567')
hebec_contact = StaffContact(
			staff_id='hebec',
			department='Section of Informatics',
			office='X1.50',
			phone='35885148'
			)
hebec_field1 = StaffField(
			staff_id='hebec',
			field='Embedded system') 
hebec_field2 = StaffField(
			staff_id='hebec',
			field='Digial eletronics') 
hebec_title1 = StaffTitle(
			staff_id='hebec',
			title='Associate Professor')
hebec_title2 = StaffTitle(
			staff_id='hebec',
			title='Project Coordinator')
hebec_title3 = StaffTitle(
			staff_id='hebec',
			title='Student Counselor')

jacno = Staff(
			staff_id='jacno',
			first_name='Jacob',
			last_name='Nordfalk',
			email='jacno@dtu.dk',
			password='1234567')
jacno_contact = StaffContact(
			staff_id='jacno',
			department='Section of Informatics',
			office='X1.53',
			phone='26206512'
			)
jacno_field1 = StaffField(
			staff_id='jacno',
			field='Android development')
jacno_field2 = StaffField(
			staff_id='jacno',
			field='Java development')
jacno_title = StaffTitle(
			staff_id='jacno',
			title='Associate Professor')

iabr = Staff(
			staff_id='iabr',
			first_name='Ian',
			last_name='Bridgwood',
			email='iabr@dtu.dk',
			password='1234567')
iabr_contact = StaffContact(
			staff_id='iabr',
			department='Section of Informatics',
			office='X1.52',
			phone='26206512'
			)
iabr_field1 = StaffField(
			staff_id='iabr',
			field='IOS development')
iabr_field2 = StaffField(
			staff_id='iabr',
			field='Unified process')
iabr_title = StaffTitle(
			staff_id='iabr',
			title='Associate Professor')

phso = Staff(
			staff_id='phso',
			first_name='Pia',
			last_name=u'Søeborg',
			email='phso@dtu.dk',
			password='1234567')
phso_contact = StaffContact(
			staff_id='phso',
			department='Section of Informatics',
			office='K1.01',
			phone='35885130'
			)
phso_title = StaffTitle(
			staff_id='phso',
			title='Study Coordinator')

s107190 = Student(
			study_no='s107190', 
			first_name='Sebastian Bryde', 
			last_name='Nielsen', 
			birthdate=datetime.date(1900,1,1), 
			email='s107190@dtu.dk',
			password='s107190')
s107190_program1= StudyProgram(
			study_no='s107190', 
			program='Admission course',
			degree_type='Admission course',
			reg_date=datetime.date(2009,9,1), 
			status='Terminated',
			earned_ECTs='0',
			reg_ECTs='0',
			tot_ECTs='210',
			graduation_date=datetime.date(2010,7,1)			
			)
s107190_program2= StudyProgram(
			study_no='s107190', 
			program='Software Technology',
			degree_type='Bachelor of Engineering',
			reg_date=datetime.date(2010,9,1), 
			status='Part-time project, part-time in house',
			earned_ECTs='180',
			reg_ECTs='30',
			tot_ECTs='210',
			graduation_date=datetime.date(2015,7,1)			
			)

s107144 = Student(
			study_no='s107144', 
			first_name='Martin', 
			last_name='Kristensen', 
			birthdate=datetime.date(1900,1,1), 
			email='s107144@dtu.dk',
			password='s107144') 
s107144_program1= StudyProgram(
			study_no='s107144', 
			program='Architectural Engineering',
			degree_type='Bachelor of Engineering',
			reg_date=datetime.date(2009,9,1), 
			status='Terminated',
			earned_ECTs='0',
			reg_ECTs='30',
			tot_ECTs='210',
			graduation_date=datetime.date(2013,2,1)			
			)
s107144_program2= StudyProgram(
			study_no='s107144', 
			program='Software Technology',
			degree_type='Bachelor of Engineering',
			reg_date=datetime.date(2010,9,1), 
			status='On campus course',
			earned_ECTs='150',
			reg_ECTs='30',
			tot_ECTs='210',
			graduation_date=datetime.date(2016,2,1)			
			)

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

record_list = [admin, hebec, hebec_contact, hebec_field1, hebec_field2, hebec_title1, hebec_title2, hebec_title3, jacno, jacno_contact, jacno_field1, jacno_field2, jacno_title, iabr, iabr_contact, iabr_field1, iabr_field2, iabr_title, phso, phso_contact, phso_title, s107190, s107190_program1, s107190_program2, s107144, s107144_program1, s107144_program2, module1, module2, module3, module4, module5]

for r in record_list:
	mydb.session.add(r)

mydb.session.commit()