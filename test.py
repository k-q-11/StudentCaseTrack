import os
import unittest
import pdb

from views import myapp, mydb
from config import basedir
from models import User

TEST_DB = 'test.db'


class AllTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        myapp.config['TESTING'] = True
        myapp.config['WTF_CSRF_ENABLED'] = False
        myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.myapp = myapp.test_client()
        mydb.create_all()

    # executed after to each test
    def tearDown(self):
        mydb.drop_all()

    ########################
    #### helper methods ####
    ########################
    def login(self, username, password):
    	return self.myapp.post('/login', 
    		data=dict(username=username, password=password), follow_redirects=True)
    
    def logout(self):
    	return self.myapp.get('/logout', follow_redirects=True)
    ###############
    #### tests ####
    ###############    


#index()  logined in user is shown overview
	def test_logged_in_user_is_shown_overview(self):
		self.login('KevinQ', '123456')
		response = self.myapp.get('/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Case overview', response.data)

#index() user not loggedin is direct to login
	def test_loggedin_required(self):
		response = self.myapp.get('/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('You need to login first.', response.data)
		
#logout() logged in user can log out
	def test_logged_in_user_can_logout(self):
		

#login() presents the login form
    def test_form_is_present_on_login_page(self):
        response = self.myapp.get('/login')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Log in here:', response.data) 

#login() the login inputs are correct format

#login() the login inputs are wrong format
	
#login() verify the user is registered

#login() if all credentials are correct, show overview

#signup() presents the signup form

#signup() the input formats correct 

#signup() the input formats incorrect

#signup() when user type a user name and/or password already exsits

#signup() creates a user in the database 

#overview() shows all the opencases

#new_case() shows add case form

#new_case() the input formats to add new case are correct

#new_case() the input formats to add new case are  incorrect

#edit_case() shows edit case form

#edit_case() the input formats to edit case form are incorrect

#edit_case() the input formats to edit case form are correct, case updated, redirect to overview
if __name__ == "__main__":
    unittest.main()
