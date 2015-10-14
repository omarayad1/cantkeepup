# tests/test_basic.py

import unittest
from app import db

from base import BaseTestCase
from app.models import Command

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
				"global", \
				"ghooo" \
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
				"global", \
				"ghooo" \
				))
		db.session.commit()
		response = self.client.get('/?q=s', 
				content_type='html/text')
		self.assertIn(b'<a href="http://www.google.com/search?q=">'
				'http://www.google.com/search?q=</a>', response.data)

if __name__ == '__main__':
	unittest.main()
