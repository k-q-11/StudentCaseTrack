from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy


myapp = Flask(__name__)
myapp.config.from_object('config')
mydb = SQLAlchemy(myapp)

from forms import ProfileForm, SignupForm, AddCaseForm, EditCaseForm
from models import User, Case

@myapp.route('/')
@myapp.route('/index', methods = ['GET', 'POST'])
def index():
	if 'logged_in' in session:
		flash('Welcome %s!' %(session['username']))
		return redirect(url_for('overview'))
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
				session['user_id'] = result.uid
				flash('You\'re logged in!')
				return redirect(url_for('overview'))
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
			myuser = User(signupForm.username.data, 
						  signupForm.email.data, 
						  signupForm.password.data)
			mydb.session.add(myuser)
			mydb.session.commit()
			flash('You\'re signed up. Please login!')
			return redirect(url_for('login'))
		else:
			flash('All fields required')
			return render_template('signup.html', form = signupForm)

@myapp.route('/overview', methods=['GET', 'POST'])
def overview():
	myopen_cases = mydb.session.query(Case).filter_by().order_by(Case.last_modified.asc())
	if myopen_cases is not None:
		return render_template('overview.html', open_cases = myopen_cases)
	else:
		return render_template('overview.html')

@myapp.route('/newcase', methods=['GET', 'POST'])
def new_case():
	addCaseForm = AddCaseForm(request.form)
	if request.method == 'GET':
		return render_template('cases.html', form = addCaseForm)
	else:
		if addCaseForm.validate_on_submit():
			mycase = Case(addCaseForm.category.data,
						  addCaseForm.resp_person.data,
						  addCaseForm.status.data,
						  session['user_id'])
			mydb.session.add(mycase)
			mydb.session.commit()
			flash('New case created!')
			return redirect(url_for('overview'))
		else:
			flash('All fields requred!')
			return redirect(url_for('new_case')) 
	
@myapp.route('/edit', methods=['GET', 'POST'])
@myapp.route('/edit/<int:mycase_id>', methods=['GET', 'POST'])
def edit_case(mycase_id):
	editCaseForm = EditCaseForm(request.form)	
	myedit_case = mydb.session.query(Case).filter_by(cid = mycase_id).first()
	if request.method == 'GET':			
		editCaseForm.resp_person.data = myedit_case.resp_person
		editCaseForm.status.data = myedit_case.status
		flash('Edit case %s' % (mycase_id) )
		return render_template('edit_case.html', form = editCaseForm, edit_case=myedit_case)
	else:
		if editCaseForm.validate_on_submit():
			myedit_case.resp_person = editCaseForm.resp_person.data
			myedit_case.status = editCaseForm.status.data
			mydb.session.commit()
			flash('Case updated!')
			return redirect(url_for('overview'))
		else:
			flash('All fields requred!')
			return redirect(url_for( 'edit_case', mycase_id = edit_case.cid) )