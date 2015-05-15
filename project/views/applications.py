#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.views.views import login_required, flash_errors
from project.forms import ProjectInfoForm, CompanyInfoForm
#from werkzeug import secure_filename
import os
from project.models import ProjectApp, Company
#from config import basedir
from project.views.views import flash_errors, allowed_file
#import psycopg2
#import binascii
#Helper
PROJ_ECTs = {
	1: 30,
	2: 15,
	3: 15,
	4: 15,
	5: 30
}
      
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

@applications_blueprint.route('/project', methods=['GET', 'POST'])
@login_required
def new_project():
	projectInfoForm = ProjectInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/projectinfo.html', form = projectInfoForm)
	else:
		if projectInfoForm.validate_on_submit():
			
			binaries = []
			#save the file both in local directory and DB
			for f in request.files.values():
				if f and allowed_file(f.filename):
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
				
			myProjectApp = ProjectApp(
				projectInfoForm.app_description.data,
				projectInfoForm.proj_module.data,
				PROJ_ECTs[projectInfoForm.proj_module.data],
				projectInfoForm.proj_title.data,
				projectInfoForm.proj_description.data,
				projectInfoForm.proj_salary.data,
				binaries[0],
				binaries[1],
				projectInfoForm.proj_s_date.data,
				projectInfoForm.proj_e_date.data
				)
			mydb.session.add(myProjectApp)
			mydb.session.commit()
			return redirect(url_for('applications.new_company'))
		else:
			flash_errors(projectInfoForm)
			return redirect(url_for('applications.new_project'))

@applications_blueprint.route('/company', methods=['GET', 'POST'])
@login_required
def new_company():
	companyInfoForm = CompanyInfoForm()#(request.form)
	if request.method == 'GET':
		return render_template('application/project/companyinfo.html', form = companyInfoForm)
	else:
		if companyInfoForm.validate_on_submit():				
			myCompany = Company(
				companyInfoForm.comp_name.data,
				companyInfoForm.comp_address.data,
				companyInfoForm.comp_department.data,
				companyInfoForm.comp_country.data,
				companyInfoForm.comp_city.data,
				companyInfoForm.comp_postcode.data,
				companyInfoForm.comp_web.data,
				companyInfoForm.comp_email.data,
				companyInfoForm.comp_phone.data
				)
			mydb.session.add(myCompany)
			mydb.session.commit()
			return redirect(url_for('applications.applications'))
		else:
			flash_errors(projectInfoForm)
			return redirect(url_for('applications.new_company'))
'''
@applications_blueprint.route('/application/<string:student_id>/projectinfo', methods=['GET', 'POST'])
@login_required
def new_project_info(student_id):
	projectInfoForm = ProjectInfoForm(request.form)

@applications_blueprint.route('/application/<string:student_id>/creditinfo', methods=['GET', 'POST'])
@applications_blueprint.route('/application/<string:student_id>/review', methods=['GET', 'POST'])		
'''
#edit project
#delete project
#check message
#checkproject applicaiton status