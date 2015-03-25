from flask import Flask, render_template, request, flash, redirect, session, url_for
from forms import ProfileForm, SignupForm
from flask.ext.sqlalchemy import SQLAlchemy


myapp = Flask(__name__)
myapp.config.from_object('config')
mydb = SQLAlchemy(myapp)

from models import User

@myapp.route('/')
@myapp.route('/index', methods = ['GET', 'POST'])
def index():
	if 'logged_in' in session:
		flash('Welcome %s!' %(session['username']))
		return render_template('overview.html')
	else:
		flash('You are not logged in')
		return redirect(url_for('login'))

@myapp.route('/logout', methods = ['GET', 'POST'])
def logout():
	if not session['logged_in']:
		return redirect(url_for('login'))
	else:
		session.pop('logged_in', None)
		session.pop('username', None)
		flash('You\'re logged out')
		return redirect(url_for('index'))

@myapp.route('/login', methods = ['GET', 'POST'])
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
				flash('You\'re logged in!')
				return render_template('overview.html')
		else:
			flash('All fields required')
			return render_template('login.html', form = loginForm)

@myapp.route('/signup', methods=['GET', 'POST'])
def signup():
	signupForm = SignupForm(request.form)
	if request.method == 'GET':
		return render_template('signup.html', form = signupForm)
	else:
		if signupForm.validate_on_submit():
			myuser = User(signupForm.username.data, signupForm.email.data, signupForm.password.data)
			mydb.session.add(myuser)
			mydb.session.commit()
			flash('You\'re signed up. Please login!')
			return redirect(url_for('login'))
		else:
			flash('All fields required')
			return render_template('signup.html', form = signupForm)