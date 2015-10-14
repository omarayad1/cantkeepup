# tests/test_basic.py

from base import BaseTestCase
from app.models import User
from flask.ext.login import current_user
from app import bcrypt

class UsersTests(BaseTestCase):

	# Ensure id is correct for the current/logged in user
	def test_get_by_id(self):
		with self.client:
			self.client.post('/login', data=dict(
				username='ghooo', password='ghooo'
			), follow_redirects=True)
			self.assertTrue(current_user.id == 2)
			self.assertFalse(current_user.id == 20)	

	# Ensure given password is correct after unhashing
	def test_check_password(self):
		user = User.query.filter_by(username='ghooo').first()
		self.assertTrue(bcrypt.check_password_hash(user.password, 'ghooo'))
		self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

class UserseViewsTests(BaseTestCase):
	# Ensure that the login page loads correctly
	def test_login_page_loads(self):
		response = self.client.get('/login')
		self.assertIn(b'Login Page', response.data)

	# Ensure errors are thrown in case of missing a required field
	def test_missing_password(self):
		with self.client:
			response = self.client.post('/login', data=dict(
				username="ghooo", password=''
			), follow_redirects=True)
			self.assertIn(b'This field is required.', response.data)

	# Ensure login behaves correctly with correct credentials
	def test_correct_login(self):
		with self.client:
			response = self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			self.assertIn(b'You were logged in', response.data)
			self.assertTrue(current_user.username == "ghooo")
			self.assertTrue(current_user.is_active)

	# Ensure login behaves correctly with incorrect credentials
	def test_incorrect_login(self):
		response = self.client.post(
			'/login',
			data=dict(username="wrong", password="wrong"),
			follow_redirects=True
		)
		self.assertIn(b'Invalid Credentials. Please try again.', response.data)

	# Ensure logout behaves correctly
	def test_logout(self):
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			response = self.client.get('/logout', follow_redirects=True)
			self.assertIn(b'You were logged out', response.data)
			self.assertFalse(current_user.is_active)

	# Ensure that logout page requires user login
	def test_logout_route_requires_login(self):
		response = self.client.get('/logout', follow_redirects=True)
		self.assertIn(b'Please log in to access this page', response.data)

	# Ensure user can register
	def test_user_registeration(self):
		with self.client:
			response = self.client.post('/register', data=dict(
				firstname='new', lastname='user', username='new',
				email='new@example.com',password='python', confirm='python'
			), follow_redirects=True)
			self.assertIn(b'Welcome new user to cantkeeup app', \
					response.data)
			self.assertTrue(current_user.username == "new")
			self.assertTrue(current_user.is_active())

	# Ensure errors are thrown during an incorrect user registration
	def test_incorrect_user_registeration(self):
		with self.client:
			response = self.client.post('/register', data=dict(
				firstname='ne', lastname='user', username='new',
				email='new',password='123', confirm=''
			), follow_redirects=True)
			self.assertIn(b'Field must be between 3 and 25 characters long.', \
					response.data)
			self.assertIn(b'Invalid email address.', response.data)
			self.assertIn(b'Field must be between 6 and 50 characters long.', \
					response.data)
			self.assertIn(b'This field is required.', response.data)
			self.assertFalse(current_user.is_active)

	# Ensure errors are thrown when username is used.
	def test_used_username_registeration(self):
		with self.client:
			response = self.client.post('/register', data=dict(
				firstname='new', lastname='user', username='ghooo',
				email='new@example.com',password='python', confirm='python'
			), follow_redirects=True)
			self.assertIn(b'Username is used!', response.data)
			self.assertFalse(current_user.is_active)

	# Ensure errors are thrown when email is used.
	def test_used_email_registeration(self):
		with self.client:
			response = self.client.post('/register', data=dict(
				firstname='new', lastname='user', username='new',
				email='ghooo@cantkeepup.com',password='python', confirm='python'
			), follow_redirects=True)
			self.assertIn(b'Email is used!', response.data)
			self.assertFalse(current_user.is_active)

if __name__ == '__main__':
	unittest.main()
