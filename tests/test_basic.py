# tests/test_basic.py

import unittest

from base import BaseTestCase

class BasicTestCase(BaseTestCase):

	# Ensure that home page opens correctly
	def test_home(self):
		response = self.client.get('/', content_type='html/text')
		self.assertIn(b'Welcome to cantkeepup app', response.data)

if __name__ == '__main__':
	unittest.main()
