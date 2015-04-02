from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from wtforms.fields.html5 import EmailField

from models import CASE_CATEGORY, CASE_STATUS

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
