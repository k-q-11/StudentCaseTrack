#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from project import mydb
from project.forms import StudentInfoForm
from project.views.views import login_required, flash_errors
from project.models import Student, StudyProgram
import pdb
################
#### config ####
################
students_blueprint = Blueprint(
    'students', __name__,
    url_prefix='/students',
    template_folder='templates',
    static_folder='static'
)

################
#### routes ####
################
@students_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def students():
	#pdb.set_trace()
	mystudentsinfo = mydb.session.query(Student)#.join(StudyProgram)
	for s in mystudentsinfo:
		print s
	return render_template('administration/students.html', students = mystudentsinfo)

@students_blueprint.route('/administration/studentinfo', methods=['GET', 'POST'])
@login_required
def new_student():#create_student(staff_id):
	studentInfoForm = StudentInfoForm(request.form)
	if request.method == 'GET':
		return render_template('administration/studentinfo.html', form = studentInfoForm)
	else:
		if studentInfoForm.validate_on_submit():
			myStudent = Student(
				studentInfoForm.study_no.data,
				studentInfoForm.first_name.data,
				studentInfoForm.last_name.data,
				studentInfoForm.date_of_birth.data,
				studentInfoForm.email.data,
				studentInfoForm.password.data,
				)
			myStudyProgram = StudyProgram(
				studentInfoForm.study_no.data,
				studentInfoForm.program.data,
				studentInfoForm.degree_type.data,
				studentInfoForm.reg_date.data,
				studentInfoForm.status.data,
				studentInfoForm.earned_ECTs.data,
				studentInfoForm.reg_ECTs.data,
				studentInfoForm.total_ECTs.data,
				studentInfoForm.graduation_date.data
				)
			mydb.session.add(myStudent)
			mydb.session.add(myStudyProgram)
			mydb.session.commit()
			return redirect(url_for('students.students'))
		else:
			flash_errors(studentInfoForm)
			return redirect(url_for('students.new_student'))