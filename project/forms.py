from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from wtforms.fields.html5 import EmailField
from datetime import date, datetime
from flask_wtf.file import FileField, FileAllowed, FileRequired


from project.models import CASE_CATEGORY, CASE_STATUS, CASE_PRIORITY, STUDY_STATUS, DEGREE_TYPE, PROGRAM, DEPARTMENT, PROJ_MODULE

class ProfileForm(Form):
	username = StringField('Username', 
		validators=[DataRequired("Please enter your user name"), 
					Length(min=6, max=25, message = 'Username input minumum 6, maximum 25 characters')]
					)
	password = PasswordField('Password', 
		validators=[DataRequired("Please enter your password"), 
					Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')]
					)
	
class SignupForm(ProfileForm):
	email = EmailField('Email', 
		validators=[DataRequired("Please enter your email"), 
					Length(min=6, max=40, message = 'Email input minumum 6, maximum 40 characters')]
					)
	repeatPassword = PasswordField('Repeat Password', 
		validators=[DataRequired("Please repeat your password"), 
					EqualTo('password', message='Password doesn\'t match')]
					)

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
	earned_ECTs = DecimalField('Current total credits in ECTs')
	reg_ECTs = DecimalField('Registered credits for this period in ECTs')
	total_ECTs = DecimalField('Total credits for the entire education')
	graduation_date = DateField('Graduation date (dd/mm/yy)', format='%d/%m/%Y')


class StaffInfoForm(Form):
	staff_id = StringField('Staff number',
			validators = [DataRequired("Please enter your staff number"),
						Length(min=2, max=20, message = 'Study number minumum 2, maximum 20 characters')]
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
	field = StringField('Field',
			validators=[DataRequired("Please enter field"),
						Length(min=0, max=100, message = 'Name input minumum 0, maximum 100 characters')]
						)
	title = StringField('Title',
			validators=[DataRequired("Please enter title"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')]
						)

class ProjectInfoForm(Form):
	app_description = TextAreaField('Application description',
					validators=[DataRequired("Please enter description"),
						Length(max=200, message = 'maximum 200 characters')])
	proj_module= SelectField('Module',
			choices = [(c, PROJ_MODULE[c]) for c in PROJ_MODULE],
			coerce=int, validators=[NumberRange(min=0)]
			)
	proj_title = StringField('Project title',
					validators=[DataRequired("Please enter title"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')])
	proj_description = TextAreaField('Project description',
					validators=[DataRequired("Please enter description"),
						Length(max=200, message = 'maximum 200 characters')])
	proj_salary = StringField('Project salary',
					validators=[DataRequired("Please enter salary"),
						Length(min=1, max=50, message = 'Name input minumum 1, maximum 50 characters')])
	proj_contract = FileField('Project contract (only pdf allowed)')#, validators=[FileRequired(), FileAllowed(['pdf'], 'Pdf only!')])
	proj_insurance = FileField('Project insurance (only pdf allowed)') #, validators=[FileRequired(), FileAllowed(['pdf'], 'Pdf only!')])
	proj_s_date = DateField('Start date (dd/mm/yy)', format='%d/%m/%Y')
	proj_e_date = DateField('End date (dd/mm/yy)', format='%d/%m/%Y')
	next_btn = SubmitField('Next')
	back_btn = SubmitField('Back')

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
	back_btn = SubmitField('Back')

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
	c_sup_title= StringField('Title',
					validators=[DataRequired(),
						Length(min=3, max=50, message = 'Name input minumum 2, maximum 50 characters')])	
	c_sup_field= StringField('Field',
					validators=[DataRequired(),
						Length(min=2, max=100, message = 'Name input minumum 2, maximum 100 characters')])
	next_btn = SubmitField('Next')
	back_btn = SubmitField('Back')

class ReviewInfoForm(Form):
	std_comment = TextAreaField('Comment',
					validators=[DataRequired()])
	std_document = FileField('Additonal document (only pdf allowed)')
	next_btn = SubmitField('Next')
	back_btn = SubmitField('Back')
	cancel_btn = SubmitField('Save and cancel')