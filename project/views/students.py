#################
#### imports ####
#################
from flask import render_template, request, flash, redirect, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from project import mydb
from project.forms import StudentInfoForm
from project.views.views import login_required, flash_errors
from project.models import Student, StudyProgram, STUDY_STATUS, PROGRAM, DEGREE_TYPE
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
	study_program_list = mydb.session.query(StudyProgram).options(joinedload(StudyProgram.student_obj)).filter(and_(StudyProgram.status!=STUDY_STATUS[10], StudyProgram.status!=STUDY_STATUS[9])).all()
	return render_template('administration/students.html', study_programs = study_program_list)

@students_blueprint.route('/administration/studentinfo', methods=['GET', 'POST'])
@login_required
def new_student():#create_student(staff_id):
	studentInfoForm = StudentInfoForm(request.form)
	if request.method == 'GET':
		return render_template('administration/studentinfo.html', form = studentInfoForm)
	else:
		if studentInfoForm.validate_on_submit():
			myStudent = Student(
				study_no=studentInfoForm.study_no.data,
				first_name=studentInfoForm.first_name.data,
				last_name=studentInfoForm.last_name.data,
				birthdate=studentInfoForm.date_of_birth.data,
				email=studentInfoForm.email.data,
				password=studentInfoForm.password.data,
				)
			myStudyProgram = StudyProgram(
				study_no=studentInfoForm.study_no.data,
				program=PROGRAM[studentInfoForm.program.data],
				degree_type=DEGREE_TYPE[studentInfoForm.degree_type.data],
				reg_date=studentInfoForm.reg_date.data,
				status=STUDY_STATUS[studentInfoForm.status.data],
				earned_ECTs=studentInfoForm.earned_ECTs.data,
				reg_ECTs=studentInfoForm.reg_ECTs.data,
				tot_ECTs=studentInfoForm.total_ECTs.data,
				graduation_date=studentInfoForm.graduation_date.data
				)
			mydb.session.add(myStudent)
			mydb.session.add(myStudyProgram)
			mydb.session.commit()
			return redirect(url_for('students.students'))
		else:
			flash_errors(studentInfoForm)
			return redirect(url_for('students.new_student'))