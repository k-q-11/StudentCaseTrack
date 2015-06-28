#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint, current_app
from flask.ext.login import login_user, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from project import mydb, bcrypt
from project.forms import StaffInfoForm, CredentialForm, NewCredentialForm
from project.views.views import login_required, flash_errors
from project.models import Student, StudyProgram, Staff, StaffContact, StaffField, StaffTitle, DEPARTMENT
from flask.ext.login import LoginManager
from project import mylogin_manager
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed
################
#### config ####
################
staffs_blueprint = Blueprint(
    'staffs', __name__,
    url_prefix='/staffs',
    template_folder='templates',
    static_folder='static'
)

from project.models import Staff
mylogin_manager.login_view = "staffs.login" # sets end point for login page


@mylogin_manager.user_loader
def load_user(user_id):
		return Staff.query.filter(Staff.staff_id == user_id).first()
################
#### routes ####
################
@staffs_blueprint.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
	#session.pop('logged_in', None)
	logout_user()
	for key in ('identity.name', 'identity.auth_type', 'staff_id'):
		session.pop(key, None)
	identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
	flash('You\'re logged out')
	return redirect(url_for('index'))

@staffs_blueprint.route('/login', methods = ['GET', 'POST'])
def login():
	loginForm = CredentialForm(request.form)
	if request.method == 'GET':
		return render_template('staff_login.html', form = loginForm)
	else:	#POST
		if loginForm.validate_on_submit():
			myuser = Staff.query.filter_by(staff_id=loginForm.staff_id.data).first()	
			if myuser is not None and bcrypt.check_password_hash(myuser.password, loginForm.password.data):		
				login_user(myuser)
				identity_changed.send(current_app._get_current_object(), identity=Identity(myuser.staff_id))
				#session['logged_in'] = True
				session['staff_id'] = myuser.staff_id # user['username'] #request.form['username']
				flash('You\'re logged in!')
				return redirect(request.args.get('next') or url_for('staffs.home'))
			else:
				flash('Invalid staff initials, password. Please try again')
				return render_template('staff_login.html', form = loginForm)
		else:
			flash_errors(loginForm)
			return render_template('staff_login.html', form = loginForm)

@staffs_blueprint.route('/changepass', methods=['GET', 'POST'])
def changepass():
	newCredentialForm = NewCredentialForm(request.form)
	if request.method == 'GET':
		return render_template('new_pass.html', form = newCredentialForm)
	else:
		if newCredentialForm.validate_on_submit():
				myuser = mydb.session.query(Staff).filter_by(staff_id=newCredentialForm.staff_id.data).first()
				if myuser is not None and bcrypt.check_password_hash(myuser.password, newCredentialForm.password.data):
					myuser.password = bcrypt.generate_password_hash(newCredentialForm.newPassword.data)				
					mydb.session.add(myuser)
					mydb.session.commit()
					login_user(myuser)
					identity_changed.send(current_app._get_current_object(), identity=Identity(myuser.staff_id))
					session['staff_id'] = myuser.staff_id
					flash('Password has been changed and you are automatically logged in!')
					# depends on the if the user is student or staff direct to differnt pages
					return redirect(request.args.get('next') or url_for('staffs.home'))
				flash('Invalid staff initials, password. Please try again!')
				return render_template('new_pass.html', form=newCredentialForm)
		else:
			flash_errors(newCredentialForm)
			return render_template('new_pass.html', form = newCredentialForm)

@staffs_blueprint.route('/staff_home', methods=['GET', 'POST'])
@login_required
def home():
	return render_template('staff_home.html')

@staffs_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def staffs():
	mystaffsinfo = mydb.session.query(Staff).join(StaffContact).join(StaffField).join(StaffTitle).all()
	return render_template('administration/staffs.html', staffs = mystaffsinfo)

@staffs_blueprint.route('/administration/staffinfo', methods=['GET', 'POST'])
@login_required
def new_staff():#create_student(staff_id):
	staffInfoForm = StaffInfoForm(request.form)
	if request.method == 'GET':
		return render_template('administration/staffinfo.html', form = staffInfoForm)
	else:
		if staffInfoForm.validate_on_submit():
			myStaff = Staff(
				staff_id=staffInfoForm.staff_id.data,
				first_name=staffInfoForm.first_name.data,
				last_name=staffInfoForm.last_name.data,
				email=staffInfoForm.email.data,
				password=staffInfoForm.password.data,
				)
			myStaffContact = StaffContact(
				staff_id=staffInfoForm.staff_id.data,
				department=DEPARTMENT[staffInfoForm.department.data],
				office=staffInfoForm.office.data,
				phone=staffInfoForm.phone.data
				)
			for field in [f.strip() for f in staffInfoForm.field.data.split(',')]:	
				myStaffField = StaffField(
					staff_id=staffInfoForm.staff_id.data,
					field=field
					)
			for title in [t.strip() for t in staffInfoForm.title.data.split(',')]:		
				myStaffTitle = StaffTitle(
					staff_id=staffInfoForm.staff_id.data,
					title=title
					)
			mydb.session.add(myStaff)
			mydb.session.add(myStaffContact)
			mydb.session.add(myStaffField)
			mydb.session.add(myStaffTitle)
			mydb.session.commit()
			return redirect(url_for('staffs.staffs'))
		else:
			flash_errors(staffInfoForm)
			return redirect(url_for('staffs.new_staff'))	