from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.fields.html5 import EmailField

class ProfileForm(Form):
	username = StringField('Username', 
		validators=[DataRequired("Please enter your user name"), Length(min=6, max=25, message = 'Username input minumum 6, maximum 25 characters')
			])
	password = PasswordField('Password', 
		validators=[DataRequired("Please enter your password"), Length(min=6, max=40, message = 'Password input minumum 6, maximum 40 characters')
			])
	
class SignupForm(ProfileForm):
	email = EmailField('Email', 
		validators=[DataRequired("Please enter your email"), Length(min=6, max=40, message = 'Email input minumum 6, maximum 40 characters')])
	repeatPassword = PasswordField('Repeat Password', validators=[DataRequired("Please repeat your password"), 
				EqualTo('password', message='Password doesn\'t match')])



