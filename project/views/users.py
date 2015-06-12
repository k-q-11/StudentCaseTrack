#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.forms import ProfileForm, SignupForm
from project.views.views import flash_errors
from project.models import User, bcrypt
from flask.ext.login import login_user, login_required, logout_user

################
#### config ####
################
users_blueprint = Blueprint(
    'users', __name__,
    url_prefix='/users',
    template_folder='templates',
    static_folder='static'
)

################
#### routes ####
################
@users_blueprint.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
	#session.pop('logged_in', None)
	logout_user()
	session.pop('username', None)
	session.pop('user_id', None)
	flash('You\'re logged out')
	return redirect(url_for('index'))

@users_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	loginForm = ProfileForm(request.form)
	if request.method == 'GET':
		return render_template('login.html', form = loginForm)
	else:	#POST
		if loginForm.validate_on_submit():
			user = User.query.filter_by(username = request.form['username']).first()	
			if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
				#session['logged_in'] = True
				login_user(user)
				session['username'] = user.username # user['username'] #request.form['username']
				session['user_id'] = user.uid
				flash('You\'re logged in!')
				return redirect(url_for('index'))
			else:
				flash('Invalid username and password')
				return render_template('login.html', form = loginForm)
		else:
			flash_errors(loginForm)
			return render_template('login.html', form = loginForm)

@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
	signupForm = SignupForm(request.form)
	if request.method == 'GET':
		return render_template('signup.html', form = signupForm)
	else:
		if signupForm.validate_on_submit():
			myuser = User(signupForm.username.data, 
						  signupForm.email.data, 
						  signupForm.password.data)
			try:
				mydb.session.add(myuser)
				mydb.session.commit()
				login_user(myuser)
				session['username'] = signupForm.username.data
				flash('You\'re signed up. and automatically logged in!')
				# depends on the if the user is student or staff direct to differnt pages
				return redirect(url_for('index'))
			except IntegrityError:
				error = "The username and/or password already exists. Please try again."
				return render_template('signup.html', form=signupForm, error=error)
		else:
			flash_errors(signupForm)
			return render_template('signup.html', form = signupForm)
		