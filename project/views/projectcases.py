#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.forms import AddCaseForm, EditCaseForm, StudentInfoForm, StaffInfoForm
from project.views.views import login_required, flash_errors
from project.models import ProjectApp

################
#### config ####
################
projectcases_blueprint = Blueprint(
    'projectcases', __name__,
    url_prefix='/projectcases',
    template_folder='templates',
    static_folder='static'
)

################
#### routes ####
################

@projectcases_blueprint.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
	myopen_cases = mydb.session.query(ProjectApp).filter_by(case_status='Opened').order_by(ProjectApp.created_date.asc())
	return render_template('projectcases.html', open_cases = myopen_cases)
	#if myopen_cases is not None:
	#	return render_template('overview.html', open_cases = myopen_cases)
	#else:
	#	return render_template('overview.html')

@projectcases_blueprint.route('/process', methods=['GET', 'POST'])
@projectcases_blueprint.route('/process/<int:mycase_id>', methods=['GET', 'POST'])
@login_required
def process_case(mycase_id):
	editCaseForm = EditCaseForm(request.form)	
	myprocess_case = mydb.session.query(Case).filter_by(cid = mycase_id).first()
	if request.method == 'GET':			
		editCaseForm.resp_person.data = myprocess_case.resp_person
		editCaseForm.status.data = myprocess_case.status
		flash('Edit case %s' % (mycase_id) )
		return render_template('edit_case.html', form = editCaseForm, process_case=myprocess_case)
	else:
		if editCaseForm.validate_on_submit():
			myprocess_case.resp_person = editCaseForm.resp_person.data
			myprocess_case.status = editCaseForm.status.data
			mydb.session.commit()
			flash('Case updated!')
			return redirect(url_for('cases.overview'))
		else:
			flash_errors(editCaseForm)
			return redirect(url_for( 'cases.process_case', mycase_id = process_case.app_id) )
	
	