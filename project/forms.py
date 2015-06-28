from datetime import date, datetime

from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField, DecimalField, TextAreaField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, Optional
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired

from project import mydb
from project.models import CASE_CATEGORY, CASE_STATUS, CASE_PRIORITY, STUDY_STATUS, DEGREE_TYPE, PROGRAM, DEPARTMENT, Module, DECISION, Staff, StaffTitle
    

class CredentialForm(Form):
	staff_id = StringField('Staff initials',
			validators = [DataRequired("Please enter your staff initials"),
						Length(min=2, max=20, message = 'Staff initials minumum 2, maximum 20 characters')]
						)
	password = PasswordField('Password', 
		validators=[DataRequired("Please enter your password"), 
					Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')]
					)
	
class NewCredentialForm(CredentialForm):
	newPassword = PasswordField('New password', 
		validators=[DataRequired("Please enter your password"), 
					Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')]
					)
	repeatNewPassword = PasswordField('Repeat new password', 
		validators=[DataRequired("Please repeat your new password"), 
					EqualTo('newPassword', message='Tow new password doesn\'t match')]
					)

class StudentSearchForm(Form):
	study_no = StringField('Study number',
			validators=[DataRequired("Please enter study number"),
						Length(min=7, max=20, message = 'Study number minumum 7, maximum 20 characters')]
						)
	search_btn = SubmitField('Search')

class StudentInfoForm(Form):
	study_no = StringField('Study number',
			validators=[DataRequired("Please enter your study number"),
						Length(min=7, max=20, message = 'Study number minumum 7, maximum 20 characters')]
						)

	first_name = StringField('First name',
			validators=[DataRequired("Please enter your first name"),
						Length(min=2, max=64, message = 'Name input minumum 2, maximum 64 characters')]
						)
	last_name = StringField('Last name',
			validators=[DataRequired("Please enter your last name"),
						Length(min=1, max=64, message = 'Name input minumum 1, maximum 64 characters')]
						)
	date_of_birth = DateField('Birthdate (dd/mm/yy)', format='%d/%m/%Y')
	email = StringField('Email',
			validators=[DataRequired("Please enter your email address"), Email(),
						Length(min=2, max=25, message = 'Name input minumum 2, maximum 254 characters')]
						)
	password = PasswordField('Password', 
		validators=[DataRequired("Please enter your password"), 
					Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')]
					)
	repeatPassword = PasswordField('Repeat Password', 
		validators=[DataRequired("Please repeat your password"), 
					EqualTo('password', message='Password doesn\'t match')]
					)
	program = SelectField('Program',
			choices = [(c, PROGRAM[c]) for c in PROGRAM],
			coerce=int, validators=[NumberRange(min=0)]
			)
	degree_type = SelectField('Degree type',
			choices = [(c, DEGREE_TYPE[c]) for c in DEGREE_TYPE],
			coerce=int, validators=[NumberRange(min=0)]
			)
	reg_date = DateField('Enroll date (dd/mm/yy)', format='%d/%m/%Y', default = date.today)
	status = SelectField('Status',
			choices = [(c, STUDY_STATUS[c]) for c in STUDY_STATUS],
			coerce=int, validators=[NumberRange(min=0)]
			)		
	earned_ECTs = DecimalField('Current total credits in ECTs', places = 1, default = 0)
	reg_ECTs = DecimalField('Registered credits for this period in ECTs', places = 1, default = 30)
	total_ECTs = DecimalField('Total credits for the entire education', places = 1, default = 210)
	graduation_date = DateField('Graduation date (dd/mm/yy)', format='%d/%m/%Y')


class StaffInfoForm(Form):
	staff_id = StringField('Staff initials',
			validators = [DataRequired("Please enter your initials"),
						Length(min=2, max=10, message = 'Staff initials minumum 2, maximum 10 characters')]
						)
	first_name =  StringField('First name',
			validators=[DataRequired("Please enter your first name"),
						Length(min=2, max=64, message = 'Name input minumum 2, maximum 64 characters')]
						)
	last_name =  StringField('Last name',
			validators=[DataRequired("Please enter your last name"),
						Length(min=2, max=64, message = 'Name input minumum 2, maximum 64 characters')]
						)
	email = StringField('Email',
			validators=[DataRequired("Please enter your email address"), Email(),
						Length(min=2, max=25, message = 'Name input minumum 2, maximum 254 characters')]
						)
	password = PasswordField('Password', 
		validators=[DataRequired("Please enter your password"), 
					Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')]
					)
	repeatPassword = PasswordField('Repeat Password', 
		validators=[DataRequired("Please repeat your password"), 
					EqualTo('password', message='Password doesn\'t match')]
					)
	department = SelectField('Department',
			choices = [(c, DEPARTMENT[c]) for c in DEPARTMENT],
			coerce=int, validators=[NumberRange(min=0)]
			)
	office = StringField('Office',
			validators=[DataRequired("Please enter office location"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')]
						)
	phone = StringField('Phone',
			validators=[DataRequired("Please enter phone number"),
						Length(min=8, max=15, message = 'Name input minumum 8, maximum 15 characters')]
						)
	field = StringField('Field (Mutiple fields seperated by comma)',
			validators=[DataRequired("Please enter field"),
						Length(min=0, max=400, message = 'Name input minumum 0, maximum 100 characters')]
						)
	title = StringField('Title (Mutiple titles seperated by comma)',
			validators=[DataRequired("Please enter title"),
						Length(min=1, max=200, message = 'Name input minumum 1, maximum 50 characters')]
						)

def list_module():
	return Module.query
class ProjectInfoForm(Form):
	app_description = TextAreaField('Application description',
					validators=[DataRequired("Please enter description"),
						Length(max=200, message = 'maximum 200 characters')])
	proj_module = QuerySelectField('Project title', 
		query_factory=list_module, get_label='module_name')
	proj_title = StringField('Project title',
					validators=[DataRequired("Please enter title"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')])
	proj_description = TextAreaField('Project description',
					validators=[DataRequired("Please enter description"),
						Length(max=200, message = 'maximum 200 characters')])
	proj_salary = StringField('Project salary',
					validators=[DataRequired("Please enter salary"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')])
	proj_contract = FileField('Project contract (only pdf allowed)')
	proj_insurance = FileField('Project insurance (only pdf allowed)')
	proj_s_date = DateField('Start date (dd/mm/yy)', format='%d/%m/%Y')
	proj_e_date = DateField('End date (dd/mm/yy)', format='%d/%m/%Y')
	next_btn = SubmitField('Next')



class CompanyInfoForm(Form):
	comp_name = StringField('Company name',
					validators=[DataRequired(),
						Length(min=2, max=50, message = 'Name input minumum 2, maximum 50 characters')])
	comp_address = StringField('Company address',
					validators=[DataRequired(),
						Length(min=5, max=95, message = 'Name input minumum 5, maximum 95 characters')])
	comp_department = StringField('Department',
					validators=[DataRequired(),
						Length(min=2, max=50, message = 'Name input minumum 2, maximum 50 characters')])
	comp_country = StringField('Country',
					validators=[DataRequired(),
						Length(min=2, max=90, message = 'Name input minumum 2, maximum 90 characters')])
	comp_city = StringField('City',
					validators=[DataRequired(),
						Length(min=1, max=60, message = 'Name input minumum 1, maximum 60 characters')])
	comp_postcode = StringField('Postcode',
					validators=[DataRequired(),
						Length(min=2, max=10, message = 'Name input minumum 2, maximum 10 characters')])
	comp_web = TextAreaField('Website',
					validators=[DataRequired()])
	comp_email = EmailField('Email',
					validators=[DataRequired(),
						Length(min=4, max=62, message = 'Name input minumum 4, maximum 62 characters')])
	comp_phone = StringField('Phone',
					validators=[DataRequired(),
						Length(min=6, max=15, message = 'Name input minumum 6, maximum 15 characters')])
	next_btn = SubmitField('Next')

class CSupervisorInfoForm(Form):
	c_sup_email = EmailField('Email',
					validators=[DataRequired(),
						Length(min=4, max=62, message = 'Name input minumum 4, maximum 62 characters')])
	c_sup_name = StringField('Comapny supervisor name',
					validators=[DataRequired(),
						Length(min=5, max=50, message = 'Name input minumum 5, maximum 50 characters')])
	c_sup_phone= StringField('Phone',
					validators=[DataRequired(),
						Length(min=6, max=15, message = 'Name input minumum 6, maximum 15 characters')])
	c_sup_title= StringField('Title (multiple titles shall be seperated by comma)',
					validators=[DataRequired(),
						Length(min=3, max=200, message = 'Name input minumum 2, maximum 50 characters')])	
	c_sup_field= StringField('Field multiple fields shall be seperated by comma',
					validators=[DataRequired(),
						Length(min=2, max=400, message = 'Name input minumum 2, maximum 100 characters')])
	next_btn = SubmitField('Next')

class ReviewInfoForm(Form):
	std_comment = TextAreaField('Comment',
					validators=[Optional()])
	std_document = FileField('Additonal document (only pdf allowed)')
	next_btn = SubmitField('Send application')
	cancel_btn = SubmitField('Save and cancel')

class ReviewCaseform(Form):
	next_btn = SubmitField('Save and complete')

def list_staff():
	return mydb.session.query(Staff).join(StaffTitle)
def display_supervisor_name(staff_obj):
	return staff_obj.first_name + ' ' + staff_obj.last_name

class ProjectProcessForm(Form):
		decision = SelectField('Decision', 
			choices= [(c, DECISION[c]) for c in DECISION],
			coerce=int, validators=[NumberRange(min=0)]
			)	
		recommend_supervisors = QuerySelectMultipleField('Recommend supervisors', query_factory=list_staff, get_label=display_supervisor_name)
		#recommend_supervisors = QuerySelectMultipleField('Recommend supervisors', 
		#query_factory=list_staff.filter(StaffTitle.title=='Associate Professor').all(), get_label=display_supervisor_name)
		staff_comment = TextAreaField('Comment',
						validators=[Optional()])
		staff_document = FileField('Additonal document (only pdf allowed)')
		next_btn = SubmitField('Next')
		

class AddCaseForm(Form):
		cid = IntegerField('Case ID')
		category = SelectField('Category', 
			choices= [(c, CASE_CATEGORY[c]) for c in CASE_CATEGORY],
			#validators=[DataRequired("Please select a category")]
			coerce=int, validators=[NumberRange(min=0)]
			)
		resp_person = StringField('Responsible person',
			validators=[DataRequired("Please enter your responsible person name"),
						Length(min=2, max=25, message = 'Name input minumum 2, maximum 25 characters')]
						)
		status  = SelectField('Status',
			choices = [(c, CASE_STATUS[c]) for c in CASE_STATUS],
			#validators=[DataRequired("Please select a status")]
			coerce=int, validators=[NumberRange(min=0)]
			)
		opened = DateField('Opened date (mm/dd/yy)')
		last_modified = DateField('Last modified date')

class EditCaseForm(Form):
		resp_person = StringField('Responsible person',
			validators=[DataRequired("Please enter your responsible person name"),
						Length(min=2, max=25, message = 'Name input minumum 2, maximum 25 characters')]
						)
		status  = SelectField('Status',
			choices = [(c, CASE_STATUS[c]) for c in CASE_STATUS],
			#validators=[DataRequired("Please select a status")]
			coerce=int, validators=[NumberRange(min=0)]
			)	