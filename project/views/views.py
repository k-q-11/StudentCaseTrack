from project import myapp, mydb
from flask import Flask, render_template, request, flash, redirect, session, url_for
from functools import wraps
from config import ALLOWED_EXTENSIONS
from flask.ext.login import login_required

##########################
#### helper functions ####
##########################

#not used
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')          

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS              

################
#### routes ####
################
@myapp.route('/')
@myapp.route('/index')
#@myapp.route('/', defaults={'first_page': 'index'})
#@myapp.route('/<first_page>')
def index():
    flash('Welcome to STADS-SCTS!' )
    return render_template('portal.html')
'''   
@login_required
def index():
    #flash('Welcome %s!' %(session['staff_id']))
    flash('Welcome!' )
    return render_template('home.html')
'''