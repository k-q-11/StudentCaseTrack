#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.forms import ProfileForm, SignupForm
from project.views.views import login_required, flash_errors
from project.models import User

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
	session.pop('logged_in', None)
	session.pop('username', None)
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
			result = User.query.filter_by(username = request.form['username'], password = request.form['password']).first()	
			if result is None:
				flash('Invalid username and password')
				return render_template('login.html', form = loginForm)
			else:
				session['logged_in'] = True
				session['username'] = result.username # result['username'] #request.form['username']
				session['user_id'] = result.uid
				flash('You\'re logged in!')
				return render_template('home.html')
		else:
			flash_errors(projectInfoForm)
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
				flash('You\'re signed up. Please login!')
				return redirect(url_for('users.login'))
			except IntegrityError:
				error = "The username and/or password already exists. Please try again."
				return render_template('signup.html', form=signupForm, error=error)
		else:
			flash_errors(projectInfoForm)
			return render_template('signup.html', form = signupForm)
		