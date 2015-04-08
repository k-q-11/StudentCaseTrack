from project import myapp, mydb
from flask import Flask, render_template, request, flash, redirect, session, url_for
from functools import wraps


##########################
#### helper functions ####
##########################
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

#not used
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')

################
#### routes ####
################
@myapp.route('/')
@myapp.route('/index')

#@myapp.route('/', defaults={'first_page': 'index'})
#@myapp.route('/<first_page>')
@login_required
def index():
    flash('Welcome %s!' %(session['username']))
    return redirect(url_for('cases.overview'))
