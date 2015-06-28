#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.views.views import login_required, flash_errors, allowed_file
from project.forms import ProjectInfoForm, CompanyInfoForm, CSupervisorInfoForm, ReviewInfoForm, StudentSearchForm
#from werkzeug import secure_filename
import os, datetime
from project.models import ProjectApp, Company, CSupervisor, CSupervisorField,CSupervisorTitle, Student
#from config import basedir
#import psycopg2
#import binascii

			
################
#### config ####
################
applications_blueprint = Blueprint(
		'applications', __name__,
		url_prefix='/applications',
		template_folder='templates',
		static_folder='static'
)

################
#### routes ####
################

@applications_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def applications():
	return render_template('application/applications.html')

@applications_blueprint.route('/student/', methods=['GET', 'POST'])
@applications_blueprint.route('/student/<next_url>', methods=['GET', 'POST'])
@login_required
def lookup_student(next_url='applications.new_project'):
	session['next_url'] = next_url
	student_search_form = StudentSearchForm()
	if request.method == 'GET':
		return render_template('student_lookup.html', form = student_search_form)
	else:
		if student_search_form.validate_on_submit():
			if mydb.session.query(Student).filter_by(study_no=student_search_form.study_no.data).first() is None:		
				return redirect(url_for('students.new_student'))
			else:
				session['applicant_study_no'] = student_search_form.study_no.data
				flash('The student is in the system!')
				return redirect(url_for(session['next_url']))
		else:
			return render_template('student_lookup.html', form = student_search_form)

@applications_blueprint.route('/project', methods=['GET', 'POST'])
@login_required
def new_project():
	project_info_form = ProjectInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/projectinfo.html', form = project_info_form)
	else:
		if project_info_form.validate_on_submit():
			binaries = []
			#save the file both in local directory and DB
			for f in request.files.values():
				if f and allowed_file(f.filename): # else throw error message
					#fn = secure_filename(f.filename)
					#save in the file system
					#file_path = os.path.join(basedir, fn)
					#f.save(file_path)
					#convert to hex format
					data = f.read()
					#data = open(f.filename, 'rb').read()
					#data = open(fn, 'rb').read()
					#binaries.append(psycopg2.Binary(data))
					#binaries.append(binascii.hexlify(data))
					binaries.append(data)					
					#f.close()	
			my_project_app = ProjectApp(
				applicant=session['applicant_study_no'],
				created_datetime=datetime.datetime.today(),
				app_description=project_info_form.app_description.data,
				proj_module=project_info_form.proj_module.data.module_id,
				proj_title=project_info_form.proj_title.data,
				proj_description=project_info_form.proj_description.data,
				proj_salary=project_info_form.proj_salary.data,
				proj_contract=project_info_form.proj_contract.data.read(),#binaries[0]
				proj_insurance=project_info_form.proj_insurance.data.read(),#binaries[1]
				proj_s_date=project_info_form.proj_s_date.data,
				proj_e_date=project_info_form.proj_e_date.data
				)			
			session.pop('applicant_study_no', None)
			session['app_id'] = my_project_app.std_save()
			return redirect(url_for('applications.new_company'))
		else:
			flash_errors(project_info_form)
			return redirect(url_for('applications.new_project'))

@applications_blueprint.route('/company', methods=['GET', 'POST'])
@login_required
def new_company():
	company_info_form = CompanyInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/companyinfo.html', form = company_info_form)
	else:			
		if company_info_form.validate_on_submit():				
			my_company = Company(
				comp_name=company_info_form.comp_name.data,
				comp_address=company_info_form.comp_address.data,
				comp_department=company_info_form.comp_department.data,
				comp_country=company_info_form.comp_country.data,
				comp_city=company_info_form.comp_city.data,
				comp_postcode=company_info_form.comp_postcode.data,
				comp_web=company_info_form.comp_web.data,
				comp_email=company_info_form.comp_email.data,
				comp_phone=company_info_form.comp_phone.data,
				)
			my_company.stf_save()#mydb.session.add(my_company)
			#mydb.session.commit()
			session['comp_name'] = company_info_form.comp_name.data
			session['comp_address'] = company_info_form.comp_address.data
			session['comp_department'] = company_info_form.comp_department.data
			return redirect(url_for('applications.new_c_supervisor'))
		else:
			flash_errors(company_info_form)
			return redirect(url_for('applications.new_company'))

@applications_blueprint.route('/csupervisor', methods=['GET', 'POST'])
@login_required
def new_c_supervisor():
	c_supervisor_info_form = CSupervisorInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/compsupervisorinfo.html', form = c_supervisor_info_form)
	else:	
		if c_supervisor_info_form.validate_on_submit():				
			c_supervisor = CSupervisor(
				c_sup_email=c_supervisor_info_form.c_sup_email.data,
				c_sup_name=c_supervisor_info_form.c_sup_name.data,
				c_sup_phone=c_supervisor_info_form.c_sup_phone.data,
				comp_name=session['comp_name'],
				comp_address=session['comp_address'],
				comp_department=session['comp_department']
				)	
			for field in [f.strip() for f in c_supervisor_info_form.c_sup_field.data.split(',')]:			
				c_supervisor_field = CSupervisorField(
					c_sup_email=c_supervisor_info_form.c_sup_email.data,
					c_sup_field=field,
					)			
				mydb.session.add(c_supervisor_field)
			for title in [t.strip() for t in c_supervisor_info_form.c_sup_title.data.split(',')]:								
				c_supervisor_title = CSupervisorTitle(
					c_sup_email=c_supervisor_info_form.c_sup_email.data,
					c_sup_title=title,					
					)
				mydb.session.add(c_supervisor_title)
			mydb.session.add(c_supervisor)						
			my_project_app = mydb.session.query(ProjectApp).filter_by(app_id=session['app_id']).first()
			my_project_app.csupervisor_obj = c_supervisor
			my_project_app.stf_save()#mydb.session.commit()
			return redirect(url_for('applications.application_review'))
		else:
			flash_errors(c_supervisor_info_form)
			return redirect(url_for('applications.new_c_supervisor'))		

@applications_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def application_review():
	review_info_form = ReviewInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/review.html', form = review_info_form)
	else:			
		if review_info_form.validate_on_submit():
			my_project_app = mydb.session.query(ProjectApp).filter_by(app_id=session['app_id']).first()
			if review_info_form.std_document.data is not None:
				f = request.files[review_info_form.std_document.name]
				if f and allowed_file(f.filename):
					my_project_app.std_document = f.read()
			if review_info_form.std_comment.data is not None:
				my_project_app.std_comment = review_info_form.std_comment.data	
			if review_info_form.cancel_btn.data:	
				my_project_app.std_save()
				return redirect(url_for('applications.application_review'))
			else:			
				my_project_app.apply()
			return redirect(url_for('applications.applications'))
		else:
			flash_errors(review_info_form)
			return redirect(url_for('applications.application_review'))		

'''
@applications_blueprint.route('/application/<string:student_id>/projectinfo', methods=['GET', 'POST'])
@login_required
def new_project_info(student_id):
	project_info_form = ProjectInfoForm(request.form)

@applications_blueprint.route('/application/<string:student_id>/creditinfo', methods=['GET', 'POST'])
@applications_blueprint.route('/application/<string:student_id>/review', methods=['GET', 'POST'])		
'''
#edit project
#delete project
#check message
#checkproject applicaiton status