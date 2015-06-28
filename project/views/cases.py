#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint, make_response, g
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.views.views import login_required, flash_errors, allowed_file
import os, datetime
from project.models import ProjectApp, Company, CSupervisor, CSupervisorField, CSupervisorTitle, DECISION, StaffTitle, Staff
from project.forms import ProjectProcessForm, ReviewCaseform
from project.access_control import project_coordinator_permission			
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

@cases_blueprint.errorhandler(403)
def unauthorized(e):
	flash('You are not authorized to access this page')
	return render_template('access_deny.html')

@cases_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def cases():
	return render_template('case/cases.html')

@cases_blueprint.route('/project/', methods=['GET', 'POST'])
@cases_blueprint.route('/project/<int:app_id>/', methods=['GET', 'POST'])
@cases_blueprint.route('/project/<int:app_id>/<command>', methods=['GET', 'POST'])
@login_required
def project_cases(app_id=None, command=None):
	if request.method == 'GET':
		if app_id is not None:
			my_case = mydb.session.query(ProjectApp).filter(ProjectApp.app_id==app_id).first()
			if command == 'Accept':
				with project_coordinator_permission.require(http_exception=403):
					my_case.accept(session['staff_id'])
			if command == 'View':
				return redirect(url_for('.view_project_case', app_id = app_id))
			if command == 'Reopen':
				with project_coordinator_permission.require(http_exception=403):
					my_case.reopen()
		orphan_cases = mydb.session.query(ProjectApp).filter(ProjectApp.case_owner==None).order_by(ProjectApp.submitted_datetime).all()
		my_open_cases = mydb.session.query(ProjectApp).filter(and_(ProjectApp.case_owner==session['staff_id'], ProjectApp.case_status!='Closed')).order_by(ProjectApp.deadline_datetime).all() 
		my_closed_cases = mydb.session.query(ProjectApp).filter(and_(ProjectApp.case_owner==session['staff_id'], ProjectApp.case_status=='Closed')).order_by(ProjectApp.close_datetime).all() 
		return render_template('case/project/projectcases.html', orphan_cases = orphan_cases, my_open_cases = my_open_cases, my_closed_cases = my_closed_cases)
	else:
		return render_template('case/cases.html')


@cases_blueprint.route('/project/process/<int:app_id>', methods=['GET', 'POST'])
@login_required
@project_coordinator_permission.require(http_exception=403)
def process_project_case(app_id):
		my_proj_case = mydb.session.query(ProjectApp).filter_by(app_id = app_id).first()
		project_process_form = ProjectProcessForm()
		if request.method == 'GET':					
			titles = [title_obj.c_sup_title for title_obj in my_proj_case.csupervisor_obj.csupervisortitle_list]
			fields = [field_obj.c_sup_field for field_obj in my_proj_case.csupervisor_obj.csupervisorfield_list]
			session['app_id'] = my_proj_case.app_id
			return render_template('case/project/caseinfo.html', case=my_proj_case, module=my_proj_case.module_obj, csupervisor=my_proj_case.csupervisor_obj, company=my_proj_case.csupervisor_obj.company_obj, titles=titles, fields=fields, form=project_process_form)							
		else:
			if project_process_form.validate_on_submit():			
				my_proj_case.app_decision=DECISION[project_process_form.decision.data]
				if project_process_form.staff_comment is not None:
					my_proj_case.staff_comment=project_process_form.staff_comment.data					
				if project_process_form.staff_document.data is not None:	
					f = request.files[project_process_form.staff_document.name]
					if f and allowed_file(f.filename):
						my_proj_case.staff_document = f.read()							
				my_proj_case.stf_save()
				return redirect(url_for('.review_project_case', app_id = session['app_id']))
			else:
				flash_errors(project_process_form)
				return redirect(url_for('.process_project_case', app_id = session['app_id']))

@cases_blueprint.route('/project/review/<int:app_id>', methods=['GET', 'POST'])
@login_required
@project_coordinator_permission.require(http_exception=403)
def review_project_case(app_id):
	review_case_form = ReviewCaseform()
	my_proj_case = mydb.session.query(ProjectApp).filter_by(app_id = app_id).first()
	if request.method == 'GET':
		supervisor_names = ['To', 'Be', 'Programmed']
		return render_template('case/project/review.html', form = review_case_form, case=my_proj_case, names=supervisor_names)
	else:
		my_proj_case.close()
		return redirect(url_for('cases.project_cases', app_id = session['app_id']))

@cases_blueprint.route('/project/download', methods=['GET', 'POST'])
@cases_blueprint.route('/project/download/<int:app_id>/<document>', methods=['GET', 'POST'])
@login_required			
def download_document(app_id, document):
	my_proj_case = mydb.session.query(ProjectApp).filter_by(app_id = app_id).first()
	if my_proj_case.app_category == 'PROJECT_APP':
		if document == 'contract':
			download_doc = my_proj_case.proj_contract
		if document == 'insurance':
			download_doc = my_proj_case.proj_insurance
	response = make_response(download_doc)
	response.headers["Content-Disposition"] = "attachment; filename=%s.pdf" %document
	return response


@cases_blueprint.route('/project/view/<int:app_id>')
@login_required
def view_project_case(app_id):
	my_proj_case = mydb.session.query(ProjectApp).filter_by(app_id = app_id).first()
	titles = [title_obj.c_sup_title for title_obj in my_proj_case.csupervisor_obj.csupervisortitle_list]
	fields = [field_obj.c_sup_field for field_obj in my_proj_case.csupervisor_obj.csupervisorfield_list]
	return render_template('case/project/casereport.html', case=my_proj_case, module=my_proj_case.module_obj, csupervisor=my_proj_case.csupervisor_obj, company=my_proj_case.csupervisor_obj.company_obj, titles=titles, fields=fields)	