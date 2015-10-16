# tests/test_basic.py

import unittest
from app import db

from base import BaseTestCase
from app.models import Command
from app.core.helpers import getGroupId, getUserId

class CommandsTests(BaseTestCase):

	# Test with nothing
	def  test_with_nothing(self):
		response = self.client.get('/?q=', content_type='html/text')
		self.assertIn(b'<a href="http://www.google.com/search?q=">'
				'http://www.google.com/search?q=</a>', response.data)

	# Test with no command id
	def  test_with_no_cmd_id(self):
		response = self.client.get('/?q=hello world', content_type='html/text')
		self.assertIn('<a href="http://www.google.com/search?q=hello%20world">'
				'http://www.google.com/search?q=hello%20world</a>',
				response.data)

	# Test with command id
	def test_with_cmd_id(self):
		db.session.add(Command( \
				"s", \
				"http://www.google.com/search?q=%s", \
				"Google Search", \
				getGroupId("global"), \
				getUserId("ghooo") \
				))
		db.session.commit()
		response = self.client.get('/?q=s hello world', 
				content_type='html/text')
		self.assertIn(b'<a href="http://www.google.com/search?q=hello%20world">'
				'http://www.google.com/search?q=hello%20world</a>',
				response.data)

	# Test with command id and empty queryText
	def test_with_cmd_id_empty_queryText(self):
		db.session.add(Command( \
				"s", \
				"http://www.google.com/search?q=%s", \
				"Google Search", \
				getGroupId("global"), \
				getUserId("ghooo") \
				))
		db.session.commit()
		response = self.client.get('/?q=s', 
				content_type='html/text')
		self.assertIn(b'<a href="http://www.google.com/search?q=">'
				'http://www.google.com/search?q=</a>', response.data)

	# Test user access his own commands only
	def test_access_own_global_commands_only(self):
		db.session.add(Command( \
				"s", \
				"http://www.google.com/search?q=%s", \
				"Google Search", \
				getUserId("ghooo"), \
				getUserId("ghooo") \
				))
		db.session.add(Command( \
				"p", \
				"http://pastie.org", \
				"Pastie", \
				getUserId("omarayad1"), \
				getUserId("omarayad1") \
				))
		db.session.add(Command( \
				"t", \
				"https://translate.google.com/#en/ar/%s", \
				"Google Translate", \
				getGroupId("global"), \
				getUserId("omarayad1") \
				))
		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)

			# access global commands
			response = self.client.get(
				'/?q=t awesome'
			)
			self.assertIn(b'<a href="https://translate.google.com/#en/ar/'
					'awesome">https://translate.google.com/#en/ar/awesome</a>', 
					response.data)

			# access own commands
			response = self.client.get(
				'/?q=s awesome'
			)
			self.assertIn(b'<a href="http://www.google.com/search?q=awesome">'
					'http://www.google.com/search?q=awesome</a>', 
					response.data)

			# can not access other users commands
			response = self.client.get(
				'/?q=p'
			)
			self.assertIn(b'<a href="http://www.google.com/search?q=p">'
					'http://www.google.com/search?q=p</a>', 
					response.data)
			
	# Test commands priority
	def test_commands_priority(self):
		db.session.add(Command( \
				"s", \
				"http://www.google.com/search?q=%s", \
				"Google Search", \
				getGroupId("global"), \
				getUserId("omarayad1") \
				))

		with self.client:
			self.client.post(
				'/login',
				data=dict(username="ghooo", password="ghooo"),
				follow_redirects=True
			)

			# access to global command
			response = self.client.get(
				'/?q=s awesome'
			)
			self.assertIn(b'<a href="http://www.google.com/search?q=awesome">'
					'http://www.google.com/search?q=awesome</a>', 
					response.data)

			# creating another command with the same cmd_id
			db.session.add(Command( \
					"s", \
					"http://www.bing.com/search?q=%s", \
					"Bing Search", \
					getUserId("ghooo"), \
					getUserId("ghooo") \
					))

			# should get the user command
			response = self.client.get(
				'/?q=s awesome'
			)
			self.assertIn(b'<a href="http://www.bing.com/search?q=awesome">'
					'http://www.bing.com/search?q=awesome</a>', 
					response.data)

if __name__ == '__main__':
	unittest.main()
