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
cases_blueprint = Blueprint(
    'cases', __name__,
    url_prefix='/cases',
    template_folder='templates',
    static_folder='static'
)

################
#### routes ####
################

@cases_blueprint.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
	myopen_cases = mydb.session.query(Case).filter_by().order_by(Case.last_modified.asc())
	return render_template('overview.html', open_cases = myopen_cases)
	#if myopen_cases is not None:
	#	return render_template('overview.html', open_cases = myopen_cases)
	#else:
	#	return render_template('overview.html')

@cases_blueprint.route('/newcase', methods=['GET', 'POST'])
@login_required
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
			return redirect(url_for('cases.overview'))
		else:
			flash_error(addCaseForm)
			return redirect(url_for('cases.new_case')) 
	
@cases_blueprint.route('/edit', methods=['GET', 'POST'])
@cases_blueprint.route('/edit/<int:mycase_id>', methods=['GET', 'POST'])
@login_required
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
			return redirect(url_for('cases.overview'))
		else:
			flash_errors(editCaseForm)
			return redirect(url_for( 'cases.edit_case', mycase_id = edit_case.cid) )
	
	