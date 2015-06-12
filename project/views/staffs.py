#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.forms import AddCaseForm, EditCaseForm, StudentInfoForm, StaffInfoForm
from project.views.views import login_required, flash_errors
from project.models import Case, Student, StudyProgram, Staff, StaffContact, StaffField, StaffTitle

################
#### config ####
################
staffs_blueprint = Blueprint(
    'staffs', __name__,
    url_prefix='/staffs',
    template_folder='templates',
    static_folder='static'
)

################
#### routes ####
################
@staffs_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def staffs():
	mystaffsinfo = mydb.session.query(Staff).join(StaffContact).join(StaffField).join(StaffTitle)
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
				staffInfoForm.staff_id.data,
				staffInfoForm.first_name.data,
				staffInfoForm.last_name.data,
				staffInfoForm.email.data,
				staffInfoForm.password.data,
				)
			myStaffContact = StaffContact(
				staffInfoForm.staff_id.data,
				staffInfoForm.department.data,
				staffInfoForm.office.data,
				staffInfoForm.phone.data
				)
			myStaffField = StaffField(
				staffInfoForm.staff_id.data,
				staffInfoForm.field.data
				)
			myStaffTitle = StaffTitle(
				staffInfoForm.staff_id.data,
				staffInfoForm.title.data
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