import os
import unittest
import pdb
from flask.ext.testing import TestCase
from project import myapp, mydb
from config import basedir
from project.models import Staff
from flask import url_for

#TEST_DB = 'test.db'


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        myapp.config['TESTING'] = True
        myapp.config['DEBUG'] = True
        myapp.config['WTF_CSRF_ENABLED'] = False
        myapp.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:s122678@localhost:5433/scts_test"
        return myapp

    def setUp(self):
        mydb.drop_all()
        mydb.create_all()
        mydb.session.add(Staff(staff_id = 'admin', first_name="Xiang", last_name="Gu", email="admin@dtu.dk", password="123456"))
        mydb.session.commit()

    def tearDown(self):
        mydb.session.remove()
        mydb.drop_all()

    ########################
    #### helper methods ####
    ########################
    
    def login(self, staff_id, password):
        return self.client.post(url_for('staffs.login'), 
            data=dict(
                staff_id=staff_id, 
                password=password), 
            follow_redirects=True)
    
    def create_user(self, staff_id, first_name, last_name, email, password):
        new_user = Staff(staff_id =staff_id, first_name = first_name, last_name = last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def change_password(self, staff_id, old_password, new_password, repeat_new_password):
        return self.client.post(url_for('staffs.changepass'),
            data=dict(
                staff_id=staff_id,
                password=old_password,
                newPassword=new_password,
                repeatNewPassword=repeat_new_password
                ),
            follow_redirects=True)        

    def logout(self):
        return self.client.get(url_for('staffs.logout'), follow_redirects=True)
'''
    def create_case(self):
        return self.client.post(
            '/newcase',
            data=dict(
                category=3, 
                resp_person='Henrik', 
                status=1, 
                user_id=1),
            follow_redirects=True) 
'''                   
    ###############
    #### tests ####
    ############### 
class MyTestCase(BaseTestCase):
#signup() presents the signup form

#signup() the input formats correct 

#signup() the input formats incorrect

#signup() when user type a user name and/or password already exsits

#index() user not loggedin is direct to login

    def test_loggedin_required(self):
        response = self.client.get(url_for('index'), follow_redirects=True )
        self.assertEquals(response.status_code, 200)
        self.assertIn('Log in', response.data)

#index()  logined in user is shown overview 
    def test_logged_in_user_is_shown_overview(self):
        response = self.login(staff_id='admin', password='123456')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Overview', response.data)

#logout() logged in user can log out
    def test_logged_in_user_can_logout(self):        
        response = self.logout()
        self.assertEquals(response.status_code, 200)
        self.assertIn('Log in', response.data)

#signup() creates a user in the database 
    def test_changepass_directs_overview(self):
        response = self.change_password('admin', '123456', '654321', '654321')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Overview', response.data)


#login() presents the login form
'''
    def test_form_is_present_on_login_page(self):
        response = self.client.get('/login')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Log in here:', response.data) 
'''
#login() the login inputs are correct format

#login() the login inputs are wrong format
	
#login() verify the user is registered

#login() if all credentials are correct, show overview



#overview() shows all the opencases

#new_case() shows add case form

#new_case() can add a case
'''
    def test_can_add_new_case(self):
        self.create_user('Henrik', 'hbm@dtu.dk', '123456')
        self.login('Henrik', '123456')
        self.client.get('/newcase', follow_redirects=True)
        response = self.create_case()
        self.assertIn()
'''
#new_case() the input formats to add new case are correct

#new_case() the input formats to add new case are  incorrect

#edit_case() shows edit case form

#edit_case() the input formats to edit case form are incorrect

#edit_case() the input formats to edit case form are correct, case updated, redirect to overview

#create_student() shows the page of new student profile

#create_student() can create a student profile

#create_student() can validates the format
    

if __name__ == "__main__":
    unittest.main()