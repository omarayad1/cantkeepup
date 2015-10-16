# tests/test_basic.py

import unittest

from base import BaseTestCase
from app import db
from app.models import Command
from app.core.helpers import getUserId, getGroupId, objectToJson

class DashboardTests(BaseTestCase):
	# ensure normal behavior
	def test_normal_behavior(self):
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			response = self.client.get(
				'/dashboard'
			)
			self.assertIn(b'Global Commands', response.data)
			self.assertEqual(response.status_code, 200)

	# ensure only accessible via logged in users
	def test_unauthenticated_access(self):
		response = self.client.get('/dashboard', follow_redirects=True)
		self.assertIn(b'Please log in to access this page.', response.data)


	def test_commands_displayed(self):
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			db.session.add(Command(
				"s",
				"http://www.google.com/search?q=%s",
				"Google Search",
				getGroupId("global"),
				getUserId("ghooo")
			))
			db.session.add(Command(
				"p",
				"http://pastie.org/",
				"Pastie",
				getUserId("ghooo"),
				getUserId("ghooo")
			))
			db.session.commit()
			response = self.client.get(
				'/dashboard'
			)
			self.assertIn(b'Global Commands', response.data)
			self.assertIn(b'User Commands', response.data)
			self.assertIn(b'Google Search', response.data)

class DatabaseURLCommandsTests(BaseTestCase):
	def basic_check(self, test_url, cmd_dict, missing_error_msg):
		# get request not available
		response = self.client.get(test_url, follow_redirects=True)
		self.assertEqual(response.status_code, 405)

		# unauthenticated access
		response = self.client.post(test_url, follow_redirects=True)
		self.assertIn(b'Please log in to access this page.', response.data)

		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)

			# missing values
			for key in cmd_dict:
				for new_value in ['',None]:
					tmp_dict = cmd_dict
					tmp_dict[key] = new_value
					response = self.client.post(
						test_url,
						data=tmp_dict
					)
					self.assertEqual(response.status_code, 400)
					self.assertEqual(response.data,missing_error_msg)

	# ensure addusercommand working according to expectations
	def test_addusercommand(self):
		test_url = '/dashboard/_addusercommand'
		self.basic_check(
			test_url, 
			dict(cmd_id='p',url="http://pastie.org",name="Pastie"),
			'A value is missing'
		)
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)

			# normal behavior
			response = self.client.post(
				test_url,
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'{"name": "Google Search", '
				'"creator": 2, "url": "http://www.google.com/search?q=%s",'
				' "cmd_id": "g", "owner": 2, "id": 1}')

			# inserting duplicates
			response = self.client.post(
				test_url,
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 400)
			self.assertEqual(response.data,'Command ID already exists')


	# ensure updateusercommand working according to expectations
	def test_updateusercommand(self):
		test_url = '/dashboard/_updateusercommand'
		self.basic_check(
			test_url, 
			dict(cmd_id='p'),
			'A value is missing'
		)
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			
			# updating non-existent command
			response = self.client.post(
				test_url,
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 400)
			self.assertEqual(response.data,'Unexpected Error')

			# normal behavior
			response = self.client.post(
				'dashboard/_addusercommand',
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'{"name": "Google Search", '
				'"creator": 2, "url": "http://www.google.com/search?q=%s",'
				' "cmd_id": "g", "owner": 2, "id": 1}')

			response = self.client.post(
				test_url,
				data=dict(cmd_id='g',url="http://www.bing.com/search?q=%s",
						name="Trolling")
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'{"name": "Trolling", "creator": 2, '
				'"url": "http://www.bing.com/search?q=%s", "cmd_id": "g", '
				'"owner": 2, "id": 1}')
			self.assertEqual(response.data,
				objectToJson(Command.query.filter_by().first()))

	# ensure deleteusercommand working according to expectations
	def test_deleteusercommand(self):
		test_url = '/dashboard/_deleteusercommand'
		self.basic_check(
			test_url, 
			dict(cmd_id='p'),
			'Command ID is missing.'
		)
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			
			# deleting non-existent command
			response = self.client.post(
				test_url,
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'success')

			# normal behavior
			response = self.client.post(
				'dashboard/_addusercommand',
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'{"name": "Google Search", '
				'"creator": 2, "url": "http://www.google.com/search?q=%s",'
				' "cmd_id": "g", "owner": 2, "id": 1}')			
			response = self.client.post(
				test_url,
				data=dict(cmd_id='g')
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data,'success')

	# ensure loadusercommand working according to expectations
	def test_loadusercommands(self):
		test_url = '/dashboard/_loadusercommands'
		# unauthenticated access
		response = self.client.get(test_url, follow_redirects=True)
		self.assertIn(b'Please log in to access this page.', response.data)

		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)
			
			# normal behavior
			self.client.post(
				'dashboard/_addusercommand',
				data=dict(cmd_id='g',url="http://www.google.com/search?q=%s",
						name="Google Search")
			)
			self.client.post(
				'dashboard/_addusercommand',
				data=dict(cmd_id='p',url="http://pastie.org",
						name="Pastie")
			)
			self.client.post(
				'dashboard/_addusercommand',
				data=dict(cmd_id='map',
						url="https://www.google.com.eg/maps/search/%s",
						name="Google Maps")
			)
			response = self.client.get(
				test_url,
				data=dict()
			)
			self.assertEqual(response.status_code, 200)
			self.assertEqual(response.data, 
				'[{"name": "Google Search", "creator": 2, '
				'"url": "http://www.google.com/search?q=%s", "cmd_id": "g", '
				'"owner": 2, "id": 1}, {"name": "Pastie", "creator": 2, '
				'"url": "http://pastie.org", "cmd_id": "p", "owner": 2, '
				'"id": 2}, {"name": "Google Maps", "creator": 2, '
				'"url": "https://www.google.com.eg/maps/search/%s", '
				'"cmd_id": "map", "owner": 2, "id": 3}]')

if __name__ == '__main__':
	unittest.main()
